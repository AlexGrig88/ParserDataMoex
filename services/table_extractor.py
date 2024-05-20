import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# словарь для хранения необходимых валютных пар с их xpath
CURRENCY = {"USD/RUB": r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[1]/div[18]/div/div[1]/a',
            "JPY/RUB": r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[1]/div[8]/div/div[1]/a'}


# список xpath до страницы с таблицей
def get_steps_to_target_page():
    return [
        r'/html/body/div[1]/div/div/div[3]/div/header/div[4]/div/div[2]/button',
        r'//*[@id="__layout"]/div/div[3]/div/header/div[5]/div[2]/div/div/div/ul/li[2]/a',
        r'/html/body/div[2]/div/div/div/div/div[1]/div/a[1]',
        r'/html/body/div[3]/div[4]/div/div/div[1]/div[1]/div/div[2]/div/div/div[3]/div[17]/div/a'
    ]


# список xpath для выставления временного интервала
def get_steps_for_timespan():
    return [
         r'//*[@id="keysParams"]',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[4]/div[1]/div[1]/div[1]',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[2]/div[4]/div/div',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[4]/div[3]/div[1]/div[1]',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/form/div[3]/span/label',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[7]/div[1]/div[1]/div[1]',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[7]/div[1]/div[1]/div[1]',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/div[3]/div[7]/div[3]/div[1]/div[3]',
         r'/html/body/div[3]/div[4]/div/div/div[1]/div/div/div/div/div[5]/form/div[4]/button'
    ]

# найти и отдать таблицы в виде html, согласно полученному списку валютных пар
def get_htmltables_for_currencies(currencies):
    driver = webdriver.Firefox()
    driver.get("https://www.moex.com/")
    time.sleep(1)
    # пробегаю до целевой таблице
    for xpath in get_steps_to_target_page():
        el = driver.find_element(By.XPATH, xpath)
        if el.is_enabled():
            el.click()
            time.sleep(1)

    tables = []

    # устанавливаю на странице необходимые временные параметры для валютной пары и извлекаю таблицу html
    for currency in currencies:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                            r'#app > form > div.ui-group-item.ui-select > div.ui-select__activator.-selected > span > svg')))
        if el.is_enabled():
            el.click()
        time.sleep(1)
        driver.find_element(By.XPATH, CURRENCY[currency]).click()
        time.sleep(1)

        for xpath in get_steps_for_timespan():
            driver.find_element(By.XPATH, xpath).click()
        time.sleep(1)
        table = driver.find_element(By.CSS_SELECTOR, ".ui-table__container > table:nth-child(1)").get_attribute(
            'outerHTML')
        tables.append(table)

    driver.close()
    return tables

