import json
import functions


# Load JSON data from a file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


# Match the app names from the entries against the valid app names
def match_apps(entries, valid_apps):
    for app_name in entries:
        if app_name in valid_apps:
            print(app_name)

def main():
    # ONLY NEEDS TO BE RUN TO POPULATE THE 'googleplay_urls.txt' FILE

    #functions.collect_urls()
    #Initialize an empty dictionary to store all apps' data
    all_apps_data = {}

   # Loop through each app url in file
   #  with open('data/take4_urls.txt', 'r') as file:
   #      for line in file:
   #          line = line.strip()  # remove any leading or trailing whitespace
   #          #app_id = line.split('=')[1]  # Extract the app ID from the URL
   #
   #          # Scrape the data safety information
   #
   #          data_safety, app_id = functions.scrape_data_safety(line)
   #          print(f"Scraping data safety information for {app_id}...")
   #
   #          # If data is found, store it under the app ID in all_apps dictionary
   #          if data_safety:
   #              all_apps_data[app_id] = data_safety
   #
   #  # Save the combined data to a JSON file
   #  functions.save_as_json(all_apps_data, 'data/google_dss2.json')
   #
   #  print("Data saved to dss.json")

    f = open('data/google_dss.json', 'r', encoding='utf-8')
    data = json.load(f)
    print(len(data))




        # Load data from JSON files
    entries = load_json('data/ppaf_data.json')
    valid_apps = load_json('data/google_dss.json')

        # Match app names and print missing ones
    match_apps(entries, valid_apps)


if __name__ == '__main__':
    main()
