#!/usr/bin/python3
"""Recursively queries Reddit API for all hot article titles."""

import requests


def recurse(subreddit, hot_list=None, after=""):
    """Return a list of all hot article titles for a subreddit recursively."""
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-recurse/1.0"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(url, headers=headers,
            params=params, allow_redirects=False)
        if response.status_code != 200:
            return None

        data = response.json()
        children = data.get("data", {}).get("children", [])
        for post in children:
            hot_list.append(post.get("data", {}).get("title"))

        after = data.get("data", {}).get("after")
        if after is None:
            return hot_list

        # Recursive call
        return recurse(subreddit, hot_list, after)

    except Exception:
        return None
