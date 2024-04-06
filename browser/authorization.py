from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from data.get_credentials import Credentials
from browser.crome_options import setting_chrome_options

class AuthorizationHandler:
    def __init__(self, browser="chrome"):
        self.driver = None
        self.browser = browser.lower()

    def setup_driver(self):
        if self.browser == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=setting_chrome_options())
        elif self.browser == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            options = webdriver.FirefoxOptions()
            # options.add_argument("--headless")
            self.driver = webdriver.Firefox(service=service, options=options)
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")

    def perform_authorization(self):
        self.driver.get(Credentials().first_login)
        login_input = self.driver.find_element("id", "login")
        login_input.send_keys(Credentials().kp_login)
        password_input = self.driver.find_element("id", "password")
        password_input.send_keys(Credentials().kp_password)
        self.driver.find_element("name", "loginbtn").click()

    def get_driver(self):
        return self.driver

    def authorize(self):
        self.setup_driver()
        self.perform_authorization()
        return self.get_driver()

if __name__ == '__main__':
    # For Chrome
    authorization_handler = AuthorizationHandler(browser="chrome")
    authorization_handler.authorize()

    # For Firefox
    authorization_handler = AuthorizationHandler(browser="firefox")
    authorization_handler.authorize()