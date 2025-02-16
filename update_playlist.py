import requests
import json

# The URL where the JSON data is located
JSON_URL = "https://raw.githubusercontent.com/byte-capsule/FanCode-Hls-Fetcher/main/Fancode_hls_m3u8.Json"
M3U_FILE = "fancode.m3u"

# Function to fetch JSON data from the URL
def fetch_json():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()  # Raise an exception if the response was unsuccessful
        return response.json()  # Return the parsed JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return None

# Function to generate the M3U playlist content
def generate_m3u(data):
    m3u_content = "#EXTM3U\n"
    for channel_id, details in data.items():
        name = details.get("name", f"Channel {channel_id}")
        url = details.get("url", "#")
        logo = details.get("logo", "")

        m3u_content += f"#EXTINF:-1 tvg-logo=\"{logo}\",{name}\n{url}\n"
    
    return m3u_content

# Function to update the M3U file
def update_playlist():
    json_data = fetch_json()
    if json_data:
        m3u_content = generate_m3u(json_data)
        with open(M3U_FILE, "w", encoding="utf-8") as file:
            file.write(m3u_content)
        print("Updated FanCode M3U successfully!")
    else:
        print("Failed to fetch JSON data.")

# Main execution
if __name__ == "__main__":
    update_playlist()
