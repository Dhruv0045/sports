import json

with open("fancode.json", "r", encoding="utf-8") as file:
    data = json.load(file)

m3u_content = "#EXTM3U\n"
for channel_id, details in data.items():
    name = details.get("name", f"Channel {channel_id}")
    url = details.get("url", "#")
    logo = details.get("logo", "")

    m3u_content += f"#EXTINF:-1 tvg-logo=\"{logo}\",{name}\n{url}\n"

with open("fancode.m3u", "w", encoding="utf-8") as file:
    file.write(m3u_content)

print("Updated FanCode M3U successfully!")
