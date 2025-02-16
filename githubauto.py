import os
import requests
import re
from github import Github

# Use direct assignment if running locally
GITHUB_TOKEN = "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"  # Replace with your token
# OR use this if using environment variables:
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("❌ GitHub Token is missing!")

REPO_NAME = "Dhruv0045/sports"
M3U_FILE_PATH = "world_wide.m3u"
JSON_URL = "https://raw.githubusercontent.com/byte-capsule/FanCode-Hls-Fetcher/main/Fancode_hls_m3u8.Json"

# --- Fetch JSON Data ---
response = requests.get(JSON_URL)
if response.status_code != 200:
    print("❌ Failed to fetch JSON data")
    exit()
data = response.json()

# --- Generate M3U ---
fancode_m3u = "#EXTM3U\n\n# ⚡ FanCode Live Matches ⚡\n\n"
for match in data.get("matches", []):
    event_cat = match.get("event_catagory", "").lower()
    if "cricket" in event_cat or "football" in event_cat:
        title = f"{match['team_1']} 🆚 {match['team_2']}"
        logo = match['team_1_flag']
        stream = match['stream_link']
        sport_emoji = "🏏" if "cricket" in event_cat else "⚽"
        fancode_m3u += f'#EXTINF:-1 tvg-id="{match["match_id"]}" tvg-name="{title}" tvg-logo="{logo}" group-title="FanCode {sport_emoji}", {title}\n{stream}\n\n'

# --- Connect to GitHub ---
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# --- Fetch or Create File ---
try:
    file = repo.get_contents(M3U_FILE_PATH)
    current_m3u = file.decoded_content.decode()
    file_sha = file.sha
    print("✅ Found existing file.")
except Exception:
    print("⚠️ File not found, creating a new one...")
    current_m3u = "#EXTM3U\n\n"
    file_sha = None

# --- Replace FanCode Section ---
pattern = r"# ⚡ FanCode Live Matches ⚡\n\n(.*?#EXTINF:-1.*?FanCode.*?https[^\n]*\n\n)*"
if re.search(pattern, current_m3u, flags=re.DOTALL):
    updated_m3u = re.sub(pattern, fancode_m3u, current_m3u, flags=re.DOTALL)
else:
    updated_m3u = current_m3u + "\n" + fancode_m3u

# --- Commit & Push Updated File ---
if file_sha:
    repo.update_file(M3U_FILE_PATH, "🔄 Auto-update FanCode section", updated_m3u, file_sha)
    print("✅ Updated existing file.")
else:
    repo.create_file(M3U_FILE_PATH, "🚀 Create new FanCode M3U file", updated_m3u)
    print("✅ Created new file.")
