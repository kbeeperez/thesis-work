import json
import functions


def main():
    # ONLY NEEDS TO BE RUN TO POPULATE THE 'googleplay_urls.txt' FILE

    #functions.collect_urls()
    # Initialize an empty dictionary to store all apps' data
    all_apps_data = {}

   # Loop through each app url in file
    with open('googleplay_urls.txt', 'r') as file:
        for line in file:
            line = line.strip()  # remove any leading or trailing whitespace
            #app_id = line.split('=')[1]  # Extract the app ID from the URL

            # Scrape the data safety information

            data_safety, app_id = functions.scrape_data_safety(line)
            print(f"Scraping data safety information for {app_id}...")

            # If data is found, store it under the app ID in all_apps dictionary
            if data_safety:
                all_apps_data[app_id] = data_safety

    # Save the combined data to a JSON file
    functions.save_as_json(all_apps_data, '1k_apps_data_safety.json')

    print("Data saved to 1k_apps_data_safety.json")


if __name__ == '__main__':
    main()
