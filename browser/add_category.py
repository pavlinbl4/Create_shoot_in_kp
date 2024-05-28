from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def select_category(category_number, driver):
    wait = WebDriverWait(driver, 10)

    # Открытие всплывающего окна
    driver.execute_script("OpenPopupWindow('ShootSubjectsAdmin.asp')")
    wait.until(EC.number_of_windows_to_be(2))

    # Переключение на всплывающее окно
    driver.switch_to.window(driver.window_handles[1])

    # Выбор категории
    category_select = Select(driver.find_element(By.ID, 'SubjectID'))
    category_select.select_by_value(category_number)

    # Нажатие кнопок "Добавить строку" и "Сохранить"
    driver.find_element(By.ID, 'addrow').click()
    driver.find_element(By.CSS_SELECTOR, '#DivSubmit input[type="submit"]').click()

    return driver
