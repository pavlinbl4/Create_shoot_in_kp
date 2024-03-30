from selenium.webdriver.support.wait import WebDriverWait

from kp_image_info_page import image_info_optimization
from make_page_link import make_history_link
from regex_tools import make_text_edit_link
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from soup_tools import get_image_links
import logging

from icecream import ic

from authorization import AuthorizationHandler

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'


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


def open_page(page_link, browser):
    browser.get(page_link)


def work_to_history(driver):
    driver.find_element(By.ID, 'ctl00_MainContent_ShootInfoForm_FullShootNumber').click()
    driver.find_element(By.CLASS_NAME, 'history-header').click()
    first_link = driver.current_url
    full_link = make_history_link(first_link)  # получаю ссылку на страницу с подробной историей
    driver.get(full_link)  # открывается новая вкладка, нужно перейти на нее
    driver.switch_to.window(driver.window_handles[0])
    return driver.page_source


def find_all_images_on_site_by_shoot_id_or_keyword(driver, shoot_id='', keyword='', only_kr=True):
    # send shoot id in its field
    driver.find_element(By.CSS_SELECTOR, '#code').clear()
    driver.find_element(By.CSS_SELECTOR, '#code').send_keys(shoot_id)  # ввожу номер съемки

    # find by keyword
    driver.find_element(By.CSS_SELECTOR, '#text').send_keys(keyword)

    # set photographer
    driver.find_element(By.CSS_SELECTOR, '#au').send_keys('Евгений Павленко')

    # set view 100 images in browser
    select = Select(driver.find_element(By.NAME, 'ps'))
    select.select_by_value('100')

    if only_kr:
        # uncheck KP images for search
        driver.find_element(By.CSS_SELECTOR, '#lib0').click()

    # click search  button
    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()

    images_number = number_of_founded_images(keyword, driver)

    return driver.current_url[:-1], images_number  # return shoot link


def end_selenium(driver):
    driver.close()
    driver.quit()


def set_keywords_to_site(good_keywords, driver):
    driver.find_element(By.NAME, 'KeywordsRus').clear()
    driver.find_element(By.NAME, 'KeywordsRus').send_keys(good_keywords)
    driver.find_element(By.NAME, 'Add').click()


def page_source_from_selenium(link, keyword, driver) -> object:
    driver.get(link)
    return driver.page_source


def get_images_count_element(driver):
    # get information from field with amount of founded images
    ic(driver.find_element(By.CSS_SELECTOR,
                           'body > table:nth-child(6) > tbody:nth-child(1) > '
                           'tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > '
                           'tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > '
                           'b:nth-child(1)'))
    # !!!! that in case - when no images found
    return driver.find_element(By.CSS_SELECTOR,
                               'body > table:nth-child(6) > tbody:nth-child(1) > '
                               'tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > '
                               'tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > '
                               'b:nth-child(1)')


def number_of_founded_images(keyword, driver):
    # take number of images from site
    try:
        images_count_element = get_images_count_element(driver)
        ic(images_count_element)

        images_count_text = images_count_element.text
        ic(images_count_text)
        images_count = int(images_count_text.replace(' ', ''))
        print(f'{green}{images_count} снимков с ключевым словом "{keyword}"{end}')
        logging.info(f'{images_count} снимков с ключевым словом "{keyword}"')
        return images_count
    except NoSuchElementException:
        logging.error(f'снимков с ключевым словом "{keyword}" не найдено')
        return 0


# function to work with all images on all pages
def images_rotator(images_number, keyword_link, driver):
    range_number = images_number // 100 + 2  # количиство страниц выданных поиском
    # for x in range(1, range_number):  # главный цикл работы программы
    for x in range(1, 100):  # главный цикл работы программы переход по страницам архива
        link = f'{keyword_link}2&pg={x}'
        html = page_source_from_selenium(link, keyword='', driver=driver)  # получаю html открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')

        for i in range(len(images_links)):  # (len(images_links)):  # обработка каждого снимка на странице

            text_edit_link, image_id, inner_id = make_text_edit_link(
                images_links[i].get('href'))  # generate edit image link

            # optimise image info
            image_info_optimization(driver, text_edit_link)


if __name__ == '__main__':
    t_driver = AuthorizationHandler().authorize()
    # check_keywords_number('велосипед', t_driver)
    print(find_all_images_on_site_by_shoot_id_or_keyword(t_driver, '', 'левакин', only_kr=True))

    # end_selenium(t_driver)
