#!/usr/bin/python3
"""Module that queries Reddit API and prints first 10 hot post titles."""

import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts for a subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "alu-top-ten/1.0"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            print("OK")  # Only printed when subreddit invalid
            return

        data = response.json()
        children = data.get("data", {}).get("children", [])

        if not children:
            print("OK")
            return

        for post in children:
            title = post.get("data", {}).get("title")
            if title:
                print(title)

    except Exception:
        print("OK")
