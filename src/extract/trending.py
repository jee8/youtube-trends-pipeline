import requests
import yaml
import os
import pandas as pd

# Load config
config_path = os.path.join(os.path.dirname(__file__), "../../pipeline_config.yaml")
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

API_KEY = config["youtube_api_key"]
REGION = config["region_code"]
MAX_RESULTS = config["max_results"]

def fetch_trending_videos():
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": REGION,
        "maxResults": MAX_RESULTS,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "items" not in data:
        raise Exception(f"Error fetching data: {data}")

    videos = []
    for item in data["items"]:
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        videos.append({
            "video_id": item["id"],
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
            "view_count": stats.get("viewCount", 0),
            "like_count": stats.get("likeCount", 0),
            "comment_count": stats.get("commentCount", 0),
            "category_id": snippet.get("categoryId", "N/A")
        })

    df = pd.DataFrame(videos)
    return df

if __name__ == "__main__":
    df = fetch_trending_videos()
    print(df.head())
    df.to_csv("data/raw/trending.csv", index=False)
    print("✅ Trending video data saved to data/raw/trending.csv")
