import requests
from bs4 import BeautifulSoup
import json


# save data in json file
def save_as_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# collect information from the data safety page
def scrape_data_safety(app_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
        # helps with identification so the website
        # doesn't automatically block it.
    }
    response = requests.get(app_url, headers=headers)  # send request to googleplay app

    if response.status_code == 200:  # check if page is up and available for scraping
        soup = BeautifulSoup(response.content, 'html.parser')  # get raw HTML and parse it
        # (considering using lxml instead of html.parser)

        # Initialize an empty dictionary to store all sections
        data_safety_info = {}

        # Find all sections that contain the jslog attribute
        sections = soup.find_all('div', class_='Mf2Txd', jslog=True)
        app_title = soup.find('div', class_="ylijCc").get_text(strip=True)

        # Iterate over each section and extract relevant data
        for section in sections:
            header = section.find('h2', class_='q1rIdc')
            if header:
                section_title = header.get_text(strip=True)  # e.g., "Data shared", "Data collected", etc.

                # Create a new entry for this section
                section_data = {}

                # Now find all subcategories within this section (e.g., "App interactions", "In-app search history")
                subcategories = section.find_all('div', class_='Vwijed')
                for subcategory in subcategories:
                    subcategory_title = subcategory.find('h3', class_='aFEzEb').get_text(strip=True)
                    subcategory_description = subcategory.find('div', class_='fozKzd').get_text(strip=True)

                    # Add the subcategory to the section
                    section_data[subcategory_title] = subcategory_description

                # Add the section to the main dictionary
                data_safety_info[section_title] = section_data

        return data_safety_info, app_title
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def scrape_ppaf():
    base_url = "http://localhost:5173"
    analysis = []

    response = requests.get(f"{base_url}/documents")
    print(f"{base_url}/documents")

    if response.status_code == 200:
        print("yay")
        soup = BeautifulSoup(response.content, 'html.parser')
        ppaf_links = soup.find_all('a', class_='_link_nazau_1')

        for x in ppaf_links:
            print(x.get("href"))


# collect urls for database
def collect_urls():
    base_url = "https://play.google.com"
    pages = []

    # array of search queries for apps
    queries = ["social", "games", "fitness", "entertainment", "messaging", "shopping", "music", "watch+tv", "tools", "gaming",
               "food", "business", "photos", "videos", "communication", "productivity", "news", "travel", "maps",
               "budgeting", "audio", "banking", "home", "nutrition", "meditation", "sleep", "learning", "languages",
               "sports", "deals", "ride", "rental", "public+transit", "calendar", "organizer", "tracker", "camera",
               "editing", "animation", "art", "talk", "journal", "retail", "stocks", "education", "ecommerce", "beauty",
               "dating", "love", "community", "security", "healthcare", "therapy", "self-help", "outdoors", "bills", "Streaming",
               "reading", "crypto", "workout", "events", "health", "charity", "parenting", "freelance", "fashion", "baking",
               "hobbies", "wellness", "adventure", "gift", "web", "gardening", "notes", "DIY", "photography", "cooking", "pets",
               "recipes", "mobile", "jobs", "projects"]

    # collect app page urls
    for term in queries:
        response = requests.get(f"{base_url}/store/search?q={term}&c=apps")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            app_links = soup.find_all('a', class_='Si6A0c Gy4nib')

            for x in app_links:
                url = f"{base_url}{x.get('href')}"
                if url in pages: # do not add any duplicate urls
                    # print(url) # to see duplicate url
                    continue
                else:
                    pages.append(url)
                    # with open("apps_urls.txt", "a") as file:  # move to top of pages link loop
                    #     file.write(f"{url}\n")
    print(len(pages))

    # use app page urls to find the data safety page url for that app, write to file
    with open("data/googleplay_urls.txt", 'r') as file:
        contents = file.read().splitlines()  # Read all lines into a list of links

    with open("data/take3_urls.txt", 'a') as f2:
        for link in pages:
            response2 = requests.get(link)

            if response2.status_code == 200:
                soup2 = BeautifulSoup(response2.content, 'html.parser')
                ds_link = soup2.find('a', class_="WpHeLc VfPpkd-mRLv6")

                if ds_link:
                    full_link = f"{base_url}{ds_link.get('href')}"
                    if full_link in contents:
                        print(f"Skipping already existing link: {full_link}")
                        continue  # Skip if link already exists
                    else:
                        # Write the new link to take2_urls.txt
                        f2.write(f"{full_link}\n")
