import requests
import json

# Define the URL of the FastAPI server
url = "http://127.0.0.1:8000/compare"

# Define the data to send in the POST request
data = {
    "ppaf_file": "ppaf_data.json",
    "gp_file": "1k_apps_data_safety.json"
}

# Send the POST request with the data
response = requests.post(url, json=data)

# Print the response from the server
print(response.status_code)  # Status code (200 indicates success)
print(response.json())  # JSON response from the server
