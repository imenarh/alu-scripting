#!/usr/bin/python3

"""
queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords
"""

import requests

def count_words(subreddit, word_list, counts=None, after=""):
    """count occurrences of keywords."""
    if counts is None:
        counts = {}

        # Initialize counts dictionary combining duplicates (case-insensitive)
        for word in word_list:
            lw = word.lower()
            counts[lw] = counts.get(lw, 0)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-count-words/1.0"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(url, headers=headers,
                                params=params, allow_redirects=False)

        if response.status_code != 200:
            return

        data = response.json()
        children = data.get("data", {}).get("children", [])

        # Process titles
        for post in children:
            title = post.get("data", {}).get("title", "")
            # Split words by spaces
            for word in title.lower().split():
                word_clean = word.strip()
                if word_clean in counts:
                    counts[word_clean] += 1

        after = data.get("data", {}).get("after")
        if after is None:
            # Sort and print results
            sorted_counts = sorted(
                [(k, v) for k, v in counts.items() if v > 0],
                key=lambda x: (-x[1], x[0])
            )
            for k, v in sorted_counts:
                print("{}: {}".format(k, v))
            return

        # Recursive call
        count_words(subreddit, word_list, counts, after)

    except Exception:
        return