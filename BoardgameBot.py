from TwitterBot import TwitterBot
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import tweepy
    import schedule
    import time
    from datetime import date, datetime
    import pandas as pd
    import numpy as np
    import requests
    from bs4 import BeautifulSoup
    import random
    import sys
    import re
    import readline
    import os

class BoardgameBot(TwitterBot):
    def __init__(self):
        super().__init__(bot_type="BoardgameBot",
                         search_terms = ["\"boardgamegeek\" OR \"boardgame\" OR \"boardgames\" OR \"board game\" OR \"board games\"", "-\"boardgame_bot\""],
                         times_to_tweet = [x + ":05" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(0,24,1)]],
                         times_to_scrape = [x + ":30" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(0,24,3)]],
                         num_to_scrape = 25)

    def get_year(self, soup):
        s = str(soup.find_all("script")[2])
        year = "".join([x for x in re.findall("yearpublished\":\"\d+", s)[0] if x.isnumeric()])
        return year

    def get_title(self, soup):
        tags = [x.get("name") for x in soup.find("head").find_all("meta")]
        content = [x.get("content") for x in soup.find("head").find_all("meta")]
        return content[tags.index("title")]

    def get_description(self, soup):
        tags = [x.get("name") for x in soup.find("head").find_all("meta")]
        content = [x.get("content") for x in soup.find("head").find_all("meta")]
        return content[tags.index("twitter:description")]

    def compose_tweet(self, link):
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = self.get_title(soup)
        year = self.get_year(soup)
        year = "".join([x for x in year if x.isnumeric()])
        desc = self.get_description(soup).replace("&quot;", "\"").replace("&ldquo;", "\"").replace("&rdquo;", "\"").replace("&amp;","&").replace("&ndash;","--")
        year = "" if year == "0" else " (" + year + ")\n\n"
        n = len(title) + len(year) + len(link) + 2
        if n + len(desc) <= 280:
            return title + year + "\n\n" + desc + "\n\n" + link
        else:
            return title + year + "\n\n" + desc[:(280-n-5)] + "..." + "\n\n" + link

    def tweet(self):
        link = requests.get("https://boardgamegeek.com/boardgame/random").url
        tweet = self.compose_tweet(link).replace("\n\n\n","\n\n")
        print(len(tweet))
        print(link)
        self.send_tweet(tweet, verbose=False)

if __name__ == "__main__":
    bot = BoardgameBot()
    # bot.tweet()
    bot.run()