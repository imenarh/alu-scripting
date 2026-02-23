#!/usr/bin/python3
"""Querying Reddit API and returns subscriber count."""

import requests


def number_of_subscribers(subreddit):
    """Return total number of subscribers for a subreddit."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "alu-subscriber-counter/1.0"}

    try:
        response = requests.get(
            url,
            headers=headers,
            allow_redirects=False
        )

        if response.status_code != 200:
            return 0

        data = response.json()
        return data.get("data", {}).get("subscribers", 0)

    except Exception:
        return 0