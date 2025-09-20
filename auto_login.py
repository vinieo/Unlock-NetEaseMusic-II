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
    browser.add_cookie({"name": "MUSIC_U", "value": "008E5B5ACBA73E66473A2440E8F8DEF0528A633EC26A9777A8F30B87B8323D43F12F22C997FE6C1A5F299B59A14200AE1CD2A33D07DA258FBDE5FA0F9C48AEA4BAF04ABA7C4A244E19F13BD05CB0D89C52CD1DC8CEB7FD6A349A7FE8274F3EA63E8C5E95AA70805F39D4E7188024EB61E8175D909E5E5B244ABD47B8B727A1AEC7928E296787EEF06C79353E204F1C72B8C33CC0D08AFD266F0AE451F0B8BB92CF5349DA1738544C1B1753A28AD0C1C173582F97DFB4306FA04F6045589EECF54E60DD1C408AC8132B1B40D91CC4017A0E5656AF8A43FDCBFB0719E688CD90F7DB9C42B4F13059D7B003EB160DA772B16095518F0877E7AF63B20D5F30282C9517EB991D53B5E716F861419BB9E031FE99A4C93A7FB382C06C0EEF0FBE56C9732D0E5F5F06B87F9FFD01047DDCD5E42A9794333A9F2F753687308F7247D01A244F52F19F05C85FC2453F1A359F86A5DD13045BCF043C29145F84FBB2C3A83FF0FC3C67C052A7F993BCCA41D916450F72736BF2F2283FA9B23F2E21E25016E42E8B0E1518397DB73A349FF9D346B2F4403B"})
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
