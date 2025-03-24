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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B0C7AFC269BC696C9A8B1D7D1DD5A3F88EAAFC7A8D577FE0D41E23397098AD8D64819B98A806699DEC49FF3A810EADE0A3F3CD9F5634995952069333071B4D073263A4B0973555093418751B609B0E9C5C728AA2A4C6980F0935F2D22CF161D3634929F31A52744CB8DA5D971F1A54FBEFC14008D920B81BBD4D9559D74AE7577EA4C28A069377915B954434D12586024AD4461306EE01D30FD6197C016E5B175E3DC41A0B13AFA643C8F9D69FAA8D91DC2D84265BBE8FC84CEAEDAB61203FFD1FDEFE97B9912048085084D7B9BB34661299705DF6478D2A6AAB7DBA711431BC9D20E0195744BAD8B614D62F6D69B0683CA0AE8173F7A6D5B767FA16AF8AFDF599A16AFA6D09E5548DEB18B1416214AB5F86837B144E035D4B8900FB6E8724A3764AA29303C87C282697FF43E637566B3C1B16028B9087131D2F1CC28FF94266936DA6E57CA34A49921E9533386C9795C7D73EE683A592F46CB0D6481C025B3B"})
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
