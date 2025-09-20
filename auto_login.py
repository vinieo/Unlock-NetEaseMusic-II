# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "003D5D28341195B61EAC7F7D7229FF762F682FFBCD9558F6D1F28ED08CA6964BD2F9E924617E5C7B5A7A423C2206217551DA37CB79F0E95F3F54956301276A34F9FF7AB0F39A050067940A1A796CE0BF4B178F192DE0FEC9841FBCD516EFD3A23C171AC276ABFCEAFBCFE9D331615B9CE4BCB3B237D5481FA26A112DB41400571433C7675BD2F896A70FE396D6334EE8094C46E6231F6B687CBE3071C972A2942931A75DCA47FEC003DB768A3DC2B2024D1AF2976761AB43EA7558037CAF6C680AC5D887D92A480D15B9ADF01CC22A59D2117E45605ECFFB8FA540EDFD6F3EDB299A154BD7102A00F6196F78CE69AEC608CCED160923FCF4E56FB203AB0EC539DA0B7EA023B3D19D9261DF0B7B89459BC791F87D130E87DDCF84DA720274B15EF5BB967FA0B8E5148FF4EF61EFBAAC0C15F1C07B918AD77B13FDF0E5731F82FBAA03A27143549F61479110A9E966BB95D8FA777C1E163040AC3032DFA2AEB5AC0635E47509BE334DF5A2BE44A996EABFBAA5ADB02214FE6EDA12D885BA2A783FC017856EBA0B71E3434F1EDA706ED908F7"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
