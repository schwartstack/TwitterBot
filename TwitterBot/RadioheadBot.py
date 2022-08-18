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

class RadioheadBot(TwitterBot):
    def __init__(self):
        super().__init__(bot_type="RadioheadBot",
                         search_terms = ["\"radiohead\" OR \"thom yorke\""],
                         times_to_tweet = [x + ":00" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(0,24,1)]],
                         times_to_scrape = [x + ":20" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(0,24,3)]],
                         num_to_scrape = 25)

    def update(self):
        super().update()
        self.update_data()

    def tweet(self):
        text = "".join(np.repeat("A",281))
        while(len(text) > 280):
            song = random.choice([x for x in self.data.lyrics if str(x) != "nan"]).replace("...","").lower().replace("efil ym fo flah.","")
            spl = song.split(". ")
            n_sentences = random.randint(1,len(spl))
            start = random.randint(0, len(spl)-n_sentences+1)
            end = start+n_sentences
            text = " ".join(spl[start:end])
        self.send_tweet(text)

if __name__ == "__main__":
    bot = RadioheadBot()
    #bot.tweet()
    bot.run()




#script to get the data:
# from lyricsgenius import Genius
# import pandas as pd
# import re
#
# genius = Genius("79AXGi_tTZnft8FrIO2405kMuJEVxyIee6o04OdW7ynEVN3PD7OAE2Gsv62PY5_X")
# radiohead = genius.search_artist('Radiohead', max_songs=200)
# lyrics = []
# titles = []
#
# for song in radiohead.songs:
#     print("Processing " + song.title + "\n")
#     newlyrics = song.lyrics
#     newlyrics = re.sub(r'\[.*\]', '', newlyrics)
#     newlyrics = re.sub(r'\d+Embed', '', newlyrics)
#     newlyrics = re.sub(r'\n\n\n\n', '\n', newlyrics)
#     newlyrics = re.sub(r'\n\n\n', '\n', newlyrics)
#     newlyrics = re.sub(r'\n\n', '\n', newlyrics)
#     lyrics.append(". ".join(newlyrics.split("\n")[1:]))
#     titles.append(song.title)
#
# pd.DataFrame({"title":titles, "lyrics":lyrics}).to_csv("~/Desktop/radiohead.csv", index = False)