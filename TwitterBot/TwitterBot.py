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


class TwitterBot:
    def __init__(self, bot_type,
                 search_terms,
                 times_to_tweet,
                 times_to_scrape,
                 num_to_scrape):
        print("Initializing bot...")
        self.bot_type = bot_type
        self.search_terms = search_terms
        self.times_to_tweet = times_to_tweet
        self.times_to_scrape = times_to_scrape
        self.num_to_scrape = num_to_scrape
        self.AUTH = []
        try:
            with open("auth/" + self.bot_type + ".txt", "r") as f:
                txt = f.readlines()
            for string in txt:
                self.AUTH.append(string.strip())
        except Exception as e:
            print("ERROR: " + str(e) + "\n")
        self.update()
        print("Hello, I am " + self.bot_type + ".\n")

    def get_api(self):
        auth = tweepy.OAuthHandler(self.AUTH[0], self.AUTH[1])
        auth.set_access_token(self.AUTH[2], self.AUTH[3])
        return tweepy.API(auth)

    def send_tweet(self, message, verbose = True):
        try:
            api = self.get_api()
            api.update_status(message)
            if verbose:
                print("\n" + self.bot_type + " is tweeting:\n" + message + "\n")
        except Exception as e:
            print("ERROR: " + str(e) + "\n")

    def update(self):
        self.update_date()

    def update_date(self):
        self.date = str(date.today())

    def update_data(self):
        updated = False
        self.data = pd.read_csv("data/" + self.bot_type + "Data.csv")
        if "item" in self.data.columns.values:
            self.data = self.data.drop_duplicates("item")
            updated = True
        if "date" in self.data.columns.values:
            self.data.date = pd.to_datetime(self.data.date)
            self.data = self.data.sort_values("date")
            updated = True
        if updated:
            self.data.to_csv("data/" + self.bot_type + "Data.csv", index = False)

    def make_first_letter_lowercase(self, string):
        return string[0].lower() + string[1:]

    def make_first_letter_uppercase(self, string):
        return string[0].upper() + string[1:]

    def add_to_list(self, item, tentative = False):
        used = "2" if tentative else "0"
        quo = "\"" if "," in item else ""
        try:
            with open("data/" + self.bot_type + "Data.csv", "a") as f:
                f.writelines(quo + item + quo + "," + used + ",\n")
        except Exception as e:
            print("ERROR: " + str(e) + "\n")

    def check_for_new_items(self):
        num_new_items = np.sum(self.data.used.values==2)
        if num_new_items:
            print("There are " + str(num_new_items) + " new items for you to vet.")

    def scrape(self, terms, num):
        print("\nBeginning scraping...\n")
        try:
            api = self.get_api()
            tweets = tweepy.Cursor(api.search_tweets,
                                   q=terms,
                                   lang="en").items(num)
        except Exception as e:
            print("ERROR: " + str(e) + "\n")
            return
        num_likes = 0
        for tweet in tweets:
            try:
                api.create_favorite(tweet.id)
                num_likes += 1
                time.sleep(random.choice([0,1,1,1,2,3,4])) #random wait time between likes so we don't look too bot-ish
            except Exception as e:
                print("ERROR: " + str(e) + "\n")
        print("done scraping. I liked " + str(num_likes) + " tweets.\n")
        self.update_num_likes(num_likes)

    def update_num_likes(self, num_likes):
        with open("data/likes.csv", "a") as f:
            f.writelines(self.bot_type + "," + ",".join(str(datetime.now()).split(" ")) + "," + str(num_likes) + "\n")

    def update_num_followers(self):
        api = self.get_api()
        num_followers = len(api.get_follower_ids())
        with open("data/followers.csv", "a") as f:
            f.writelines(self.bot_type + "," + self.date + "," + str(num_followers) + "\n")

    def run(self):
        print("running " + self.bot_type + "...\n")
        schedule.every().hour.do(self.update)
        schedule.every().day.at("23:59").do(self.update_num_followers)
        for t in self.times_to_tweet:
            try:
                schedule.every().day.at(t).do(self.tweet)
                print(self.bot_type + " will tweet at " + t)
            except Exception as e:
                print("ERROR: " + str(e) + "\n")
        for t in self.times_to_scrape:
            try:
                schedule.every().day.at(t).do(self.scrape, self.search_terms, self.num_to_scrape)
                print(self.bot_type + " will scrape twitter at " + t)
            except Exception as e:
                print("ERROR: " + str(e) + "\n")
        while True:
            schedule.run_pending()
            time.sleep(60)