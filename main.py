
import time
import asyncio
from datetime import datetime, timedelta, timezone
import chromedriver_autoinstaller
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from aiogram import Bot, Dispatcher, types
import os
import json

# Путь к конфигурационному файлу
CONFIG_FILE = "config.json"

# Значения по умолчанию для конфигурации
DEFAULT_CONFIG = {
    "TOKEN": "",  # Токен Telegram бота
    "url": "",  # Ссылка на приложение
    "times": True,  # Работа по графику
    "click_times": [  # Список времени для графика
        "2:00:00", "3:00:00", "5:00:00", "6:30:00",
        "13:30:00", "14:30:00", "18:00:00", "20:00:00"
    ],
    "screenshot_path": "screenshot.png"  # Путь для сохранения скриншота
}

# Функция для загрузки или создания конфигурационного файла
def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        # Если файл существует, загрузить значения
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)
            print("Конфигурация загружена.")
    else:
        # Если файла нет, создать его с значениями по умолчанию
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4, ensure_ascii=False)
            print("Создан новый конфигурационный файл с настройками по умолчанию, заполните его")

        config = DEFAULT_CONFIG

    return config

# Загрузка конфигурации
config = load_or_create_config()

# Использование значений конфигурации
TOKEN = config["TOKEN"]
url = config["url"]
times = config["times"]
click_times = config["click_times"]
screenshot_path = config["screenshot_path"]

if config == DEFAULT_CONFIG:
    exit()



dp = Dispatcher()

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists


driver = webdriver.Chrome(options=options)
driver.get(url)


def capture_screenshot():
    """Создает скриншот страницы."""
    try:
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        print(f"Ошибка при создании скриншота: {e}")

def click_button():
    """Выполняет клик по кнопке на странице."""
    try:
        time.sleep(10)  # Ожидание загрузки страницы
        element = driver.find_element(By.TAG_NAME, "body")  # Укажите нужный селектор
        action = ActionChains(driver)
        action.move_to_element_with_offset(element, 0, -65).click().perform()
        print("Клик выполнен!")
    except Exception as e:
        print(f"Ошибка при клике: {e}")



async def wait_and_click(target_time: str):
    """Ожидает до заданного времени (МСК) и выполняет клик."""

    while True:
        # Получаем текущее UTC время и переводим в МСК
        now_utc = datetime.now(timezone.utc)
        now_msk = now_utc.astimezone(timezone(timedelta(hours=3)))  # МСК = UTC+3

        # Преобразуем target_time (например, "02:00:00") в объект времени
        target_time_obj = datetime.strptime(target_time, "%H:%M:%S").time()

        # Создаем объект datetime для целевого времени на основе текущей даты
        target_datetime = datetime.combine(now_msk.date(), target_time_obj, tzinfo=timezone(timedelta(hours=3)))

        # Если текущее время уже прошло целевое, переносим на следующий день
        if now_msk >= target_datetime:
            target_datetime += timedelta(days=1)

        # Вычисляем время ожидания в секундах
        wait_time = (target_datetime - now_msk).total_seconds()

        # Лог ожидания
        print(f"Ожидание до {target_time} (МСК): {wait_time:.2f} секунд")

        # Ожидание до нужного времени
        await asyncio.sleep(wait_time)

        # Выполнение клика (замените click_button на вашу реализацию)
        click_button()

        # После клика можно выйти из цикла, если нужно только один раз
        # break



async def schedule_all_clicks():
    """Планирует клики для всех времен из списка одновременно."""
    is_between_times(click_times)
    tasks = [asyncio.create_task(wait_and_click(time)) for time in click_times]
    await asyncio.gather(*tasks)

def is_between_times(click_times):
    click_times = [datetime.strptime(t, "%H:%M:%S").time() for t in click_times]
    now = datetime.now().time()  # Текущее время

    # Идем по парам времени (включение/выключение)
    for i in range(0, len(click_times), 2):
        start, end = click_times[i], click_times[i + 1]
        # Проверяем, находится ли текущее время в интервале
        if start <= now <= end:
            click_button()
            break

@dp.message(Command(commands=['screen']))
async def send_screenshot(message: Message):
    """Обрабатывает команду /screen и отправляет скриншот."""
    await message.answer("Создаю скриншот, подождите...")
    # Создаем скриншот
    capture_screenshot()
    # Отправляем файл
    await message.answer_document(types.FSInputFile(screenshot_path))
async def main():
    """Главная асинхронная функция для запуска бота и кликов."""
    if times:
        asyncio.create_task(schedule_all_clicks())  # Запуск планирования всех кликов
    else:
        click_button()
    print("Бот запущен...")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  # Запуск главного цикла событий
