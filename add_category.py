from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


def select_category(category_number, driver):
    wait = WebDriverWait(driver, 10)
    driver.execute_script("OpenPopupWindow('ShootSubjectsAdmin.asp')")
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    category = Select(driver.find_element(By.ID, 'SubjectID'))
    category.select_by_value(category_number)
    driver.find_element(By.XPATH, '//*[@id="addrow"]').click()
    driver.find_element(By.XPATH, '//*[@id="DivSubmit"]/input[1]').click()
    return driver
