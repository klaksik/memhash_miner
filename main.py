import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Укажите ссылку
url = ""



screenshot_path = "screenshot.png"
# Настройка WebDriver (замените путь на ваш драйвер)
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
try:
    # Открыть сайт
    driver.get(url)

    # Укажите время ожидания для полной загрузки
    time.sleep(10)

    # Найдите область, где нужно кликнуть (например, элемент <div>)
    element = driver.find_element(By.TAG_NAME, "body")  # Замените селектор на нужный

    # Получение координат для клика
    action = ActionChains(driver)
    action.move_to_element_with_offset(element, 0, -65).click().perform()  # Координаты (100, -20)

    # Ожидание после клика
    time.sleep(5)

    # Сделать скриншот
    driver.save_screenshot(screenshot_path)
    print(f"Отчет сохранён: {screenshot_path}")
    while True:
        time.sleep(60)
        driver.save_screenshot(screenshot_path)
        print(f"Отчет сохранён: {screenshot_path}")


except Exception as e:
    print(f"Ошибка: {e}")

finally:
    driver.quit()