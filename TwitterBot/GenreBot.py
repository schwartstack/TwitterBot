#(obscure OR unusual OR "lesser known" OR niche) (genres OR genre) (music OR musical)

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

class GenreBot(TwitterBot):
    def __init__(self):
        super().__init__(bot_type="GenreBot",
                         search_terms = ["\"(obscure OR unusual OR \"lesser known\" OR niche OR random OR specific)\"",
                                         "\"(genres OR genre OR style OR styles)\"",
                                         "\"(music OR musical OR musician OR band OR song OR album)\"",
                                         "-\"obscuregenre\""],
                         times_to_tweet = [x + ":00" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(9,24,12)]],
                         times_to_scrape = ["08:40","18:40","02:40"],
                         num_to_scrape = 100)

    def update(self):
        super().update()
        self.update_data()

    def compose_tweet(self, url):
        try:
            title = re.sub("\\(.+\\)","",url.split("/")[-1].replace("_", " "))
            response = requests.get(url)
            html = BeautifulSoup(response.text, 'html.parser')
            body = html.find("body").findAll("p")
            for p in html.find("body").findAll("p"):
                if title.lower() in p.getText().lower():
                    tweet = re.sub("\\[\\d+\\]", "", p.getText())[:(275-len(url))] + "...\n\n" + url
                    break
            return tweet
        except Exception as e:
            print("ERROR: " + str(e) + "\n")

    def tweet(self):
        print("\nBeginning tweeting...\n")
        print("we have tweeted " + str(len([x for x in self.data.used.values if x == 1])) + " times.")
        print("there are " + str(len([x for x in self.data.used.values if x == 0])) + " unused links.")

        #pick a random unused url
        tweet = ""
        while tweet == "":
            rand = random.choice([i for i in range(len(self.data.used)) if self.data.used.values[i] == 0])
            print("selecting index " + str(rand))
            url = self.data.item.values[rand]
            #compose the tweet
            tweet = self.compose_tweet(url)
        try:
            #send the tweet
            self.send_tweet(tweet)

            #set the chosen url to "used"
            self.data.used.values[rand] = 1
            self.data.date.values[rand] = date.today()
            self.data = self.data.sort_values("date")

            #save the new csv with the chosen url marked as used
            self.data.to_csv("data/" + self.bot_type + "Data.csv", index = False)
        except Exception as e:
            print("ERROR: " + str(e) + "\n")

        search_term = re.sub("\\(.+\\)","",url.split("/")[-1].replace("_", " "))
        try:
            self.scrape([search_term], 100)
        except Exception as e:
            print("ERROR: " + str(e) + "\n")

if __name__ == "__main__":
    bot = GenreBot()
    #bot.tweet()
    bot.run()















#code to get data:
# lists = ["https://en.wikipedia.org/wiki/List_of_styles_of_music:_A–F",
#          "https://en.wikipedia.org/wiki/List_of_styles_of_music:_G–M",
#          "https://en.wikipedia.org/wiki/List_of_styles_of_music:_N–R",
#          "https://en.wikipedia.org/wiki/List_of_styles_of_music:_S–Z"]
#
# for list in lists:
#     print("processing " + list + "\n")
#     response = requests.get(list)
#     html = BeautifulSoup(response.text, 'html.parser')
#     with open("data/GenreBotData.csv", "a") as f:
#         for tag in html.select("body")[0].select("li")[45:]:
#             try:
#                 link = tag.find("a").get("href")
#             except Exception as e:
#                 pass
#             if link is not None:
#                 if "List_of_styles_of_music" in link:
#                     break
#                 else:
#                     if "#" not in link:
#                         f.writelines("https://en.wikipedia.org" + link + ",0,\n")
# print("done.")
