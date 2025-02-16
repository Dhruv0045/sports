import os
import requests
import re
from github import Github

# --- 🔐 Configuration ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Use GitHub Secrets
REPO_NAME = "Dhruv0045/sports"
M3U_FILE_PATH = "world_wide.m3u"
JSON_URL = "https://raw.githubusercontent.com/byte-capsule/FanCode-Hls-Fetcher/main/Fancode_hls_m3u8.Json"

# --- Step 1: Fetch JSON Data ---
response = requests.get(JSON_URL)
if response.status_code != 200:
    print("❌ Failed to fetch JSON data")
    exit()

data = response.json()

# --- Step 2: Generate New FanCode M3U Section ---
fancode_m3u = "#EXTM3U\n\n# ⚡ FanCode Live Matches ⚡\n\n"

for match in data.get("matches", []):
    event_cat = match.get("event_catagory", "").lower()
    if "cricket" in event_cat or "football" in event_cat:
        title = f"{match['team_1']} 🆚 {match['team_2']}"
        logo = match['team_1_flag']
        stream = match['stream_link']
        sport_emoji = "🏏" if "cricket" in event_cat else "⚽"
        fancode_m3u += f'#EXTINF:-1 tvg-id="{match["match_id"]}" tvg-name="{title}" tvg-logo="{logo}" group-title="FanCode {sport_emoji}", {title}\n{stream}\n\n'

# --- Step 3: Fetch Current M3U File from GitHub ---
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

try:
    file = repo.get_contents(M3U_FILE_PATH)
    current_m3u = file.decoded_content.decode()
except Exception as e:
    print(f"⚠️ Could not fetch M3U file: {e}")
    current_m3u = "#EXTM3U\n\n"  # Create a new file if not found

# --- Step 4: Replace Only FanCode Section ---
pattern = r"# ⚡ FanCode Live Matches ⚡\n\n(.*?#EXTINF:-1.*?FanCode.*?https[^\n]*\n\n)*"
if re.search(pattern, current_m3u, flags=re.DOTALL):
    updated_m3u = re.sub(pattern, fancode_m3u, current_m3u, flags=re.DOTALL)
else:
    updated_m3u = current_m3u + "\n" + fancode_m3u  # If no section exists, append it

# --- Step 5: Commit & Push Updated File ---
repo.update_file(M3U_FILE_PATH, "🔄 Auto-update FanCode section", updated_m3u, file.sha)
print("✅ FanCode section updated successfully!")
