#!/usr/bin/python3
import requests


def count_words(subreddit, word_list, after=None, counts=None, mult=None):
    """Print sorted keyword counts (case-insensitive) from all hot titles."""
    if not isinstance(subreddit, str) or not isinstance(word_list, list):
        return

    if counts is None or mult is None:
        counts = {}
        mult = {}
        for w in word_list:
            if isinstance(w, str) and w != "":
                lw = w.lower()
                mult[lw] = mult.get(lw, 0) + 1
                counts.setdefault(lw, 0)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "alche-scripting:api_advanced:v1.0 (by u/yourusername)"}
    params = {"limit": 100, "after": after}

    try:
        res = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10
        )
        if res.status_code != 200:
            return

        data = res.json().get("data", {})
        children = data.get("children", [])
        next_after = data.get("after")

        for child in children:
            title = child.get("data", {}).get("title", "")
            for token in title.lower().split():
                if token in counts:
                    counts[token] += 1

        if next_after is not None:
            return count_words(subreddit, word_list, next_after, counts, mult)

        results = []
        for word, c in counts.items():
            total = c * mult.get(word, 0)
            if total > 0:
                results.append((word, total))

        results.sort(key=lambda x: (-x[1], x[0]))

        for word, total in results:
            print(f"{word}: {total}")

    except (requests.RequestException, ValueError):
        return

