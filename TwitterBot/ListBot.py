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

class ListBot(TwitterBot):
    def __init__(self):
        super().__init__(bot_type="ListBot",
                         search_terms = ["\"wikipedia\"",
                                         "\"list\"",
                                         "-\"itweetlists\""],
                         times_to_tweet = [x + ":00" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(0,24,6)]],
                         times_to_scrape = ["11:25","23:25"],
                         num_to_scrape = 100)

    def update(self):
        super().update()
        self.update_data()
        self.check_for_new_items()

    def get_title(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find("title").get_text().replace(" - Wikipedia", "")
            subtitle = ""
            if "#" in url:
                subtitle = " (" + url.split("#")[-1].replace("_"," ") + ")"
            if "Wikipedia:" in title:
                title = title.replace("Wikipedia:", "")
            if "Category:" in title:
                    title = title.replace("Category:", "")
                    title = self.make_first_letter_lowercase(title)
                    title = "List of " + title
            return title + subtitle
        except Exception as e:
            print("ERROR: " + str(e) + "\n")

    def compose_tweet(self, url):
        try:
            return(self.get_title(url) + "\n\n" + url)
        except Exception as e:
            print("ERROR: " + str(e) + "\n")

    def scrape(self, terms, num):
        print("\nBeginning scraping...\n")
        n_likes = 0
        try:
            api = self.get_api()
            tweets = tweepy.Cursor(api.search_tweets,
                                   q=terms,
                                   lang="en").items(num)
        except Exception as e:
            print("ERROR: " + str(e) + "\n")
            return
        for tweet in tweets:
            try:
                api.create_favorite(tweet.id)
                n_likes += 1
            except Exception as e:
                print("ERROR: " + str(e) + "\n")
            # try:
            #     api.create_friendship(screen_name = tweet.user.screen_name)
            # except Exception as e:
            #     print("ERROR: " + str(e) + "\n")

            links = tweet.entities['urls']
            if links:
                for link in links:
                    redirected_link = link['expanded_url']
                    print(redirected_link)
                    if "wikipedia" in redirected_link.lower() and "list" in redirected_link.lower():
                        print("\nI FOUND A LIST!\n" + redirected_link + "\n")
                        print(tweet.user.screen_name + " tweeted:\n" + tweet.text + "\n")
                        try:
                            self.add_to_list(redirected_link.replace("en.m.","en.").replace("w/index.php?","wiki/"), tentative=True)
                            self.update_data()
                        except Exception as e:
                            print("ERROR: " + str(e) + "\n")
        print("done scraping...\n")
        self.update_num_likes(n_likes)

    def tweet(self):
        print("\nBeginning tweeting...\n")
        print("we have tweeted " + str(len([x for x in self.data.used.values if x == 1])) + " times.")
        print("there are " + str(len([x for x in self.data.used.values if x == 0])) + " unused links.")
        print("there are " + str(len([x for x in self.data.used.values if x == 2])) + " unchecked new links.\n")

        #pick a random unused url
        rand = random.choice([i for i in range(len(self.data.used)) if self.data.used.values[i] == 0])
        print("selecting index " + str(rand))
        url = self.data.item.values[rand]

        try:
            #compose the tweet
            tweet = self.compose_tweet(url)

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
    #
    # #delete this after i'm done unfollowing people
    # def unfollow(self, n = 20):
    #     api = bot.get_api()
    #     friends = api.get_friend_ids()
    #     for friend in friends[:n]:
    #         print("unfollowing " + str(friend))
    #         api.destroy_friendship(user_id=friend)
    #         time.sleep(random.randint(20,100))

if __name__ == "__main__":
    bot = ListBot()
    #bot.tweet()
    bot.run()