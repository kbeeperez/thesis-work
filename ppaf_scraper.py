import requests
from bs4 import BeautifulSoup
import json
import time

import functions

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def get_link(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/91.0.4472.124 Safari/537.36'
               # helps with identification so the website
               # doesn't automatically block it.
               }

    res = requests.get(url, headers=headers)  # send request to google play app

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        app_title = soup.find('div', class_="ylijCc").get_text(strip=True)
        policy = soup.find_all('a', class_='GO2pB')

        # for x in policy:
        #     th = x.get("href")
        #     print(th)

        if len(policy) > 1:
            print(app_title)
            link = policy[1].get('href')
        else:
            link = f"no policy found for: {url}"

    return link, app_title


def main():
    ########### List of Google Play Store app URLs to scrape, populates privacy policy txt file.
    # with open('data/privacy_policy_links_take3.txt', 'a', encoding='utf-8') as policy:
    #     with open('data/take4_urls.txt', 'r') as file:
    #         for line in file:
    #             line = line.strip()
    #             # print(line)
    #             link, title = get_link(line)  # get privacy policy link from google play page
    #             # print(link)
    #
    #             policy.write(f"{title}\n{link}\n")
    #             print(f"stored: {link}")
    ############################LOGIN TO PPAF########################################
    ppafurl_auth = "http://localhost:5173/auth"  # url for documents page for PPAF
    driver_path = r"C:\Users\Katherine Perez\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(ppafurl_auth)

    user = driver.find_element(By.XPATH, '//input[@placeholder="a.user@privacy.matters"]')
    password = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
    #
    user.send_keys('k@3.com')  # Replace with the name you want to input
    password.send_keys("testtest")
    #
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Or use By.ID, By.CLASS_NAME, etc.

    # # Click the submit button
    submit_button.click()
    time.sleep(2)

    new_url = "http://localhost:5173/documents"  # The URL you want to navigate to after login
    driver.get(new_url)  # This will redirect you to the new URL
    time.sleep(20)
    print(driver.current_url)  # check that we are at URL

    # # ################################scarpe document cards, block later############################
    all_apps_data = {}
    count = 0

    # get document ids from http://127.0.0.1:8000/docs, the Privacify API

    f = open('data/ids_4.json', encoding='utf-8')
    data = json.load(f)

    for x in data:
        count += 1;
        # print(x['id']) #url ID
        driver.get(f"http://localhost:5173/documents/{x['id']}")  # go to url
        print(driver.current_url)  # check that we are at URL
        time.sleep(2)

        page_html2 = driver.page_source  # collect HTML from page
        soup2 = BeautifulSoup(page_html2, 'html.parser')  # parse page

        appid = soup2.find('h1', class_="m-8a5d1357 mantine-Title-root")  # find title
        app_id = appid.get_text(strip=True)  # e.g., "SnapChat"
        print(app_id)  # check card title

        priv_data = {}  # current section data
        sections = soup2.find_all('div', class_='m-1b7284a3 mantine-Paper-root')  # find sections "Data shared, etc."
        sections = sections[:3]  # only use the first 3 sections of the card (data shared/ collected / security)
        for i in sections:
            header = i.find('h4', class_="m-8a5d1357 mantine-Title-root")  # get section title
            if header:
                title = header.get_text(strip=True)  # e.g., "Data shared"
                print(title)
                info = i.find('ul', class_="m-abbac491 mantine-List-root").get_text(strip=True)
                print(info)

                priv_data[title] = info

            all_apps_data[app_id] = priv_data
        functions.save_as_json(all_apps_data, 'data/LAST.json')
        print(count)
    #####################################scapre document cards#######################################


    # ################# feed into PPAF ##################################
    # with open("data/privacy_policy_links_take3.txt", 'r', encoding='utf-8') as file:
    #     lines = file.readlines()
    #
    #     for i in range(0, len(lines), 2):  # Increment by 2 to grab pairs
    #         _id = lines[i].strip()  # Extract the ID (remove any extra spaces or newlines)
    #         _link = lines[i + 1].strip()  # Extract the Link
    #
    #         if "no policy" in _link:
    #             continue
    #
    #         print(f"Processing ID: {_id}, Link: {_link}")
    #
    #         id2 = driver.find_element(By.XPATH, '//input[@placeholder="Example Privacy Policy"]')
    #         url = driver.find_element(By.XPATH, '//input[@placeholder="https://privacy.policies.matter"]')
    #         time.sleep(2)
    #
    #         id2.send_keys(_id)
    #         url.send_keys(_link)
    #         time.sleep(3)
    #
    #         submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Or use By.ID, By.CLASS_NAME
    #         submit_button.click()
    #         time.sleep(50)
    #
    #         driver.refresh()
    #         time.sleep(7)
    ######################################### FEED INTO PPAF ###################################################


if __name__ == '__main__':
    main()
