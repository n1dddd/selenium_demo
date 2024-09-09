import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

with open("data.json", "w") as f:
    json.dump([], f)

def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)

        file_data.append(new_data)

        file.seek(0)

        json.dump(file_data, file, indent=4)

with webdriver.Chrome(service=service, options=chrome_options) as browser:
    browser.get("https://www.amazon.ca/s?k=3d+filament&crid=1JMPL9UUO1STU&sprefix=3d+filament%2Caps%2C71&ref=nb_sb_noss_1")

    isNextDisabled = False
    
    while not isNextDisabled:
        
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))

        elemnt_list=browser.find_element(By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")

        items = elemnt_list.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        for item in items:
            title  = item.find_element(By.TAG_NAME, "h2").text
            price = "No price found"
            img = "No image found"
            link = item.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute('href')
            try:
                price = item.find_element(By.CLASS_NAME, 'a-price').text.replace("\n", ".")
            except:
                pass

            try:
                img = item.find_element(By.CSS_SELECTOR, '.s-image').get_attribute("src")
                
            except:
                pass

            print("Title: " +title)
            print("Price: " +price)
            print("Image URL: " +img)
            print("Link: " + link + "\n")

            write_json({
                "title": title,
                "price": price,
                "image": img,
                "link": link
            })

        try:
            next_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "s-pagination-next")))

            next_class = next_btn.get_attribute('class')

            if "disabled" in next_class:
                isNextDisabled = True
            else:
                browser.find_element(By.CLASS_NAME, 's-pagination-next').click()
        except Exception as e:
            print(e, "Error here")
            isNextDisabled = True