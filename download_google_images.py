import time
import base64
from io import BytesIO
import re
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from PIL import Image

import config

DOWNLOADED_IMAGES_PATH = config.DOWNLOADED_IMAGES_PATH

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service
)

SLEEP_TIME = 2

def download_google_images(search_query: str, number_of_images=500) -> None:
    '''Download google images with this function\n
       Takes -> search_query, number_of_images\n
       Returns -> None
    '''
    def scroll_to_bottom():
        '''Scroll to the bottom of the page
        '''
        last_height = driver.execute_script(
            'return document.body.scrollHeight')
        while True:
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(SLEEP_TIME)

            new_height = driver.execute_script(
                'return document.body.scrollHeight')
            try:
                element = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='.YstHxe input'
                )
                element.click()
                time.sleep(SLEEP_TIME)
            except:
                pass

            if new_height == last_height:
                break

            last_height = new_height

    url = 'https://images.google.com/'

    driver.get(
        url=url
    )

    box = driver.find_element(
        by=By.XPATH,
        value="//input[contains(@class,'gLFyf gsfi')]"
    )

    box.send_keys(search_query)
    box.send_keys(Keys.ENTER)
    time.sleep(SLEEP_TIME)

    scroll_to_bottom()
    time.sleep(SLEEP_TIME)

    img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'rg_i Q4LuWd')]"
    )

    print(f'Totla images -> {len(img_results)}')

    count = 0

    for img_result in img_results:
        try:
            WebDriverWait(
                driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    img_result
                )
            )
            img_result.click()
            time.sleep(SLEEP_TIME)

            actual_imgs = driver.find_elements(
                by=By.XPATH,
                value="//img[contains(@class,'n3VNCb')]"
            )

            src = ''

            for actual_img in actual_imgs:
                if 'https://encrypted' in actual_img.get_attribute('src'):
                    pass
                elif 'http' in actual_img.get_attribute('src'):
                    src += actual_img.get_attribute('src')
                    break
                else:
                    pass

            for actual_img in actual_imgs:
                if src == '' and 'base' in actual_img.get_attribute('src'):
                    src += actual_img.get_attribute('src')

            if 'https://' in src:
                file_path = f'{DOWNLOADED_IMAGES_PATH}/{re.sub(pattern=" ", repl="_", string=search_query)}_image_{count}.jpeg'
                result = requests.get(src)
                open(file_path, 'wb').write(result.content)
                try:
                    img = Image.open(file_path)
                    img = img.convert('RGB')
                    img.save(file_path, 'JPEG')
                    print('Image saved from https.')
                except:
                    print('Bad image.')
                    os.unlink(file_path)
                    count -= 1
            else:
                img_data = src.split(',')
                file_path = f'{DOWNLOADED_IMAGES_PATH}/{re.sub(pattern=" ", repl="_", string=search_query)}_image_{count}.jpeg'
                try:
                    img = Image.open(BytesIO(base64.b64decode(img_data[1])))
                    img = img.convert('RGB')
                    img.save(file_path, 'JPEG')
                    print('Image saved from Base64.')
                except:
                    print('Bad image.')
                    count -= 1
        except ElementClickInterceptedException as e:
            count -= 1
            print(e)
            print('Image is not clickable.')

        count += 1
        if count == number_of_images:
            break


tags = config.TAGS_PATH
with open(file=tags, mode='r') as file:
    tags = json.load(file)

tags = tags['tags']

NUMBER_OF_IMAGES_PER_CLASS = config.NUMBER_OF_IMAGES_PER_CLASS

for tag in tags:
    print(f'Started downloading the images for the {tag} tag.')
    download_google_images(
        search_query=tag,
        number_of_images=NUMBER_OF_IMAGES_PER_CLASS
    )
    print(f'Finished downloading the images for the {tag} tag.')

driver.quit()
