package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	"context"
	"os/signal"
	"syscall"

	"github.com/chromedp/chromedp"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

const (
	ConfigFile      = "config.json"
	DefaultHeadless = true
)

type Config struct {
	Token          string   `json:"TOKEN"`
	URL            string   `json:"url"`
	Times          bool     `json:"times"`
	ClickTimes     []string `json:"click_times"`
	ScreenshotPath string   `json:"screenshot_path"`
}

var defaultConfig = Config{
	Token:          "",
	URL:            "",
	Times:          true,
	ClickTimes:     []string{"2:00:00", "3:00:00", "5:00:00", "6:30:00", "13:30:00", "14:30:00", "18:00:00", "20:00:00"},
	ScreenshotPath: "screenshot.png",
}

func loadOrCreateConfig() Config {
	if _, err := os.Stat(ConfigFile); err == nil {
		file, err := os.Open(ConfigFile)
		if err != nil {
			log.Fatalf("Error opening config file: %v", err)
		}
		defer file.Close()

		var config Config
		if err := json.NewDecoder(file).Decode(&config); err != nil {
			log.Fatalf("Error decoding config file: %v", err)
		}
		fmt.Println("Configuration loaded.")
		return config
	}

	file, err := os.Create(ConfigFile)
	if err != nil {
		log.Fatalf("Error creating config file: %v", err)
	}
	defer file.Close()

	if err := json.NewEncoder(file).Encode(defaultConfig); err != nil {
		log.Fatalf("Error encoding default config: %v", err)
	}

	fmt.Println("New configuration file created. Please fill it.")
	return defaultConfig
}

func captureScreenshot(ctx context.Context, path string) {
	var buf []byte
	if err := chromedp.Run(ctx, chromedp.FullScreenshot(&buf, 100)); err != nil {
		log.Printf("Error capturing screenshot: %v", err)
		return
	}

	if err := os.WriteFile(path, buf, 0644); err != nil {
		log.Printf("Error saving screenshot to file: %v", err)
	}
}

func clickButton(ctx context.Context) {
	log.Println("Ожидание загрузки страницы...")
	time.Sleep(10 * time.Second)

	// Выполняем клик
	err := chromedp.Run(ctx,
		chromedp.Query("body", chromedp.AtLeast(0)),
		chromedp.MouseClickXY(960, 396),
	)

	if err != nil {
		log.Printf("Ошибка при клике: %v", err)
		return
	}

	log.Println("Клик выполнен!")
}
func waitAndClick(ctx context.Context, targetTime string) {
	for {
		now := time.Now().UTC().Add(3 * time.Hour) // Convert to MSK
		target, err := time.Parse("15:04:05", targetTime)
		if err != nil {
			log.Printf("Error parsing target time: %v", err)
			return
		}

		targetTime := time.Date(now.Year(), now.Month(), now.Day(), target.Hour(), target.Minute(), target.Second(), 0, now.Location())
		if now.After(targetTime) {
			targetTime = targetTime.Add(24 * time.Hour) // Move to the next day
		}

		waitDuration := targetTime.Sub(now)
		log.Printf("Waiting until %s (MSK): %v", targetTime.Format("15:04:05"), waitDuration)
		time.Sleep(waitDuration)

		clickButton(ctx)
	}
}

func scheduleAllClicks(ctx context.Context, times []string) {
	var wg sync.WaitGroup
	for _, t := range times {
		wg.Add(1)
		go func(target string) {
			defer wg.Done()
			waitAndClick(ctx, target)
		}(t)
	}
	wg.Wait()
}

func main() {
	config := loadOrCreateConfig()
	if config.Token == "" || config.URL == "" {
		return
	}

	opts := append(chromedp.DefaultExecAllocatorOptions[:],
		chromedp.Flag("headless", DefaultHeadless),
		chromedp.Flag("no-sandbox", true),
		chromedp.Flag("disable-dev-shm-usage", true),
	)

	// Добавляем обработку сигналов завершения
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	// Создаем контекст с отменой
	ctx, cancel := context.WithCancel(context.Background())

	// Создаем allocator с правильным закрытием
	allocatorCtx, allocatorCancel := chromedp.NewExecAllocator(ctx, opts...)
	defer allocatorCancel()

	// Создаем контекст браузера
	browserCtx, browserCancel := chromedp.NewContext(allocatorCtx)
	defer browserCancel()

	// Горутина для обработки сигналов завершения
	go func() {
		<-sigChan
		log.Println("Получен сигнал завершения, закрываем браузер...")
		browserCancel()
		allocatorCancel()
		cancel()
		os.Exit(0)
	}()

	// Добавляем установку размера окна после создания контекста
	if err := chromedp.Run(browserCtx, chromedp.EmulateViewport(1920, 1080)); err != nil {
		log.Fatalf("Error setting viewport: %v", err)
	}

	if err := chromedp.Run(browserCtx, chromedp.Navigate(config.URL)); err != nil {
		log.Fatalf("Error opening URL: %v", err)
	}

	if config.Times {
		go scheduleAllClicks(browserCtx, config.ClickTimes)
	} else {
		clickButton(browserCtx)
	}

	// Telegram bot setup
	bot, err := tgbotapi.NewBotAPI(config.Token)
	if err != nil {
		log.Fatalf("Error creating Telegram bot: %v", err)
	}
	log.Printf("Bot authorized as %s", bot.Self.UserName)

	updateConfig := tgbotapi.NewUpdate(0)
	updateConfig.Timeout = 60
	updates := bot.GetUpdatesChan(updateConfig)

	for update := range updates {
		if update.Message != nil && update.Message.IsCommand() {
			switch update.Message.Command() {
			case "screen":
				captureScreenshot(browserCtx, config.ScreenshotPath)
				msg := tgbotapi.NewDocument(update.Message.Chat.ID, tgbotapi.FilePath(config.ScreenshotPath))
				bot.Send(msg)
			}
		}
	}
}
