import time
import asyncio
from datetime import datetime, timedelta, timezone
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from aiogram import Bot, Dispatcher, types

# подвязка к телеграм боту для отслеживания работы
TOKEN = ""

# ссылка на приложение
url = ""

# работа по графику
times = True

# Список времени для графика (в формате HH:MM:SS, МСК) (обязательно парное количество и в возрастающем списке по времени суток, 1 значение - 1 клик на кнопку)
click_times = ["2:00:00", "3:00:00", "5:00:00", "6:30:00", "13:30:00", "14:30:00", "18:00:00", "20:00:00"]

# Настройка Telegram бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

screenshot_path = "screenshot.png"
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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

@dp.message_handler(commands=['screen'])
async def send_screenshot(message: types.Message):
    """Отправляет скриншот в ответ на команду /screen."""
    capture_screenshot()
    await message.answer("Создаю скриншот, подождите...")
    await message.answer_document(open(screenshot_path, 'rb'))

async def main():
    """Главная асинхронная функция для запуска бота и кликов."""
    if times:
        asyncio.create_task(schedule_all_clicks())  # Запуск планирования всех кликов
    else:
        click_button()
    print("Бот запущен...")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())  # Запуск главного цикла событий
