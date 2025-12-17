#!/usr/bin/python3
import requests


def top_ten(subreddit):
    """Print the first 10 hot post titles for a given subreddit, else None."""
    if not isinstance(subreddit, str) or subreddit == "":
        print(None)
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "alche-scripting:api_advanced:v1.0 (by u/yourusername)"}
    params = {"limit": 10}

    try:
        res = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10
        )

        if res.status_code != 200:
            print(None)
            return

        payload = res.json()
        children = payload.get("data", {}).get("children", [])

        for child in children[:10]:
            title = child.get("data", {}).get("title")
            if title is not None:
                print(title)

    except (requests.RequestException, ValueError):
        print(None)
