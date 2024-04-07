from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Настраиваем опции Chrome для работы в режиме headless
options = Options()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")


# Устанавливаем ChromeDriver



service = Service(ChromeDriverManager().install())
print(service)

# Инициализируем драйвер с указанными опциями
driver = webdriver.Chrome(service=service, options=options)

# Открываем страницу в браузере
driver.get("http://example.com")

# Выводим заголовок страницы
print(driver.title)

# Закрываем браузер
driver.quit()