#!/usr/bin/python3
"""2-recurse: Recursively fetch all hot article titles from a subreddit."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of titles of all hot posts for a subreddit."""
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "alche-scripting:api_advanced:v1.0 (by u/yourusername)"
    }
    params = {
        "limit": 100,
        "after": after
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        children = data.get("children", [])

        for child in children:
            hot_list.append(child.get("data", {}).get("title"))

        after = data.get("after")

        if after is not None:
            return recurse(subreddit, hot_list, after)

        return hot_list

    except (requests.RequestException, ValueError):
        return None

