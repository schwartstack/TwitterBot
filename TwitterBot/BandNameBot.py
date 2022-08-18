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

class BandNameBot(TwitterBot):
    def __init__(self):
        super().__init__(bot_type="BandNameBot",
                         search_terms = ["band name"],
                         times_to_tweet = [x + ":30" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(0,24,1)]],
                         times_to_scrape = [x + ":15" for x in ["0" + str(x) if x < 10 else str(x) for x in np.arange(0,24,3)]],
                         num_to_scrape = 25)

    def update(self):
        super().update()
        self.update_data()

    def update_data(self):
        super().update_data()
        self.data = self.data.assign(word = lambda df : df.word.map(lambda word : str(word).lower()))
        with open("data/bandNameConstructions.txt", "r") as f:
            cons = f.readlines()
        self.constructions = [x for x in cons if "#" not in x]
        with open("data/bandNameGenres.txt", "r") as f:
            genres = f.readlines()
        self.genres = [x.replace("\n", "") for x in genres]
        self.cities = pd.read_csv("data/bandNameCities.csv")

    def tweet(self):
        construction = random.choice(self.constructions).replace("\n", "")
        text = self.compose_tweet(construction)
        print(construction)
        #print(text)
        self.send_tweet(text)


    def compose_tweet(self, construction):
        if "[]" in construction:
            construction = construction.replace("The []", random.choice([x for x in self.constructions if x[:3] == "The"]))

        while "ANY" in construction:
            construction = construction.replace("ANY", self.word("ANY"), 1)
        while "NOUN[s]" in construction:
            construction = construction.replace("NOUN[s]", self.pluralize(self.word("NOUN")), 1)
        while "VERB[ers]" in construction:
            construction = construction.replace("VERB[ers]", self.pluralize(self.nounize(self.word("VERB"))), 1)
        while "VERB[ing]" in construction:
            construction = construction.replace("VERB[ing]", self.gerundize(self.word("VERB")), 1)

        for pos in self.data.pos.unique():
            while pos in construction:
                construction = construction.replace(pos, self.word(pos), 1)

        return " ".join([self.make_first_letter_uppercase(word) for word in construction.split(" ")]) + "\n\n" + self.get_background_info(construction)

    def get_genre(self):
        choices = sorted(random.choices(self.genres, k = random.choices([2,3], weights=[.9,.1], k=1)[0]),key=lambda x : len(x))
        return self.remove_first_dupes(" ".join(sorted(choices,key=lambda x : len(x))).replace(".", " "))

    def remove_first_dupes(self, s):
        sep = [char for char in s if char in [" ", "-"]]
        sep.append("")
        temp = s.replace("-", " ")
        spl = temp.split(" ")
        rem = []
        for i in range(len(spl)):
            if spl[i] in spl[i+1:]:
                rem.append(i)
        return "".join([spl[i]+sep[i] for i in range(len(spl)) if i not in rem])


    # def order_score(self, word):
    #     score = []
    #     for genre in self.genres:
    #         genre_split = genre.replace("-"," ").split(" ")
    #         if genre_split.count(word) > 0:
    #             score.append(genre_split.index(word)/len(genre_split))
    #     return np.mean(score) + .1*len(score)

    def get_city(self):
        cnt = random.choices(["United States","Canada","United Kingdom","Australia",""], weights = [60, 10, 10, 5, 15], k = 1)[0]
        if cnt == "":
            city = self.cities[self.cities.country != "United States"].sample(1)
            return city.city.values[0] + ", " + city.country.values[0]
        else:
            city = self.cities[self.cities.country == cnt].sample(1)
        if cnt == "United States":
            return city.city.values[0] + ", " + city.admin_name.values[0]
        elif cnt == "Canada":
            return city.city.values[0] + ", " + city.admin_name.values[0] + ", " + city.country.values[0]
        else:
            return city.city.values[0] + ", " + city.country.values[0]

    def get_background_info(self, bandName):
        genre = self.get_genre()
        city = self.get_city()
        if genre[0] in ["a","e","i","o","u"]:
            s = "(an "
        else:
            s = "(a "
        if bandName[-1] == "s" or bandName[:3] == "The":
            group_word = random.choices(["band","group","duo","trio","quartet","ensemble","orchestra","boy band","girl group","jam band"],weights=[0.41382,0.24342,0.14319,0.08423,0.04955,0.02915,0.01714,0.01008,0.00593,0.00349],k=1)[0]
        else:
            group_word = random.choices(["band","group","artist","duo","trio","quartet","singer-songwriter","ensemble","orchestra","boy band","girl group","jam band"],weights=[0.33592,0.22395,0.1493,0.09953,0.06636,0.04424,0.02949,0.01966,0.01311,0.00874,0.00583,0.00388],k=1)[0]


        return s + genre + " " + group_word + " from " + city + ")"


    def pluralize(self, noun):
        attempts = [noun + "s", noun + "es", noun[:-1] + "ies", noun]
        for attempt in attempts:
            if attempt in self.data.word.values:
                return attempt

    def gerundize(self, verb):
        attempts = [verb + "ing", verb + verb[-1] + "ing", verb[:-1] + "ing", verb[:-2] + "ing", verb]
        for attempt in attempts:
            if attempt in self.data.word.values:
                return attempt

    def nounize(self, verb):
        attempts = [verb + verb[-1] + "er", verb + "r", verb + "er", verb]
        for attempt in attempts:
            if attempt in self.data.word.values:
                return attempt

    def word(self, pos):
        if pos == "ANY":
            return random.choice(self.data.word.values)
        else:
            return random.choice(self.data.word.values[self.data.pos == pos])



if __name__ == "__main__":
    bot = BandNameBot()
    #bot.tweet()
    bot.run()













###R code to generate data:
# common = read.table("https://raw.githubusercontent.com/schwartstack/wordle/main/english-common-words.txt", header = F) %>% pull(V1) %>% as.character()
# fem = read.table("https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt", skip = 5) %>% pull(V1) %>% as.character()
# mal = read.table("https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt", skip = 5) %>% pull(V1) %>% as.character()
# unk = read.table("http://www.mieliestronk.com/corncob_lowercase.txt", header = F) %>% pull(V1) %>% as.character()
# tit = c("Dr.", "Mr.", "Miss", "Mrs.", "Lady", "Lord", "Ms.", "Sir", "Mother", "Father", "Brother", "Sister", "Cousin", "Uncle", "Aunt", "Earl", "Capt.", "Captain", "Sergeant", "Sgt.", "Colonel", "General", "Officer", "Detective", "Chief", "King", "Queen", "Prince", "Princess", "Duke", "Private", "President", "Emperor")
#
# tidytext::parts_of_speech %>%
#     filter(word %in% unk) %>%
#     filter(pos != "Plural") %>%
#     filter(pos != "Noun Phrase") %>%
#     filter(word %in% common) %>%
#     mutate(pos = case_when(pos == "Noun" ~ "NOUN",
#                            pos == "Adjective" ~ "ADJ",
#                            pos == "Adverb" ~ "ADV",
#                            pos == "Conjunction" ~ "CONJ",
#                            pos == "Definite Article" ~ "DEFAR",
#                            pos == "Interjection" ~ "INTER",
#                            pos == "Preposition" ~ "PREP",
#                            pos == "Pronoun" ~ "PRO",
#                            grepl("Verb", pos) ~ "VERB",
#                            TRUE ~ pos)) %>%
#     distinct %>%
#     rbind(data.frame(word = c(fem,mal), pos = rep("NAME", length(c(fem,mal))))) %>%
#     rbind(data.frame(word = setdiff(unk, .$word),
#     pos = "UNK")) %>%
#     rbind(data.frame(word = tit, pos = rep("TITLE", length(tit)))) %>%
#     write.csv("~/Documents/TwitterBot/data/BandNameBotData.csv",row.names = F)

###python code to get genres:
# url = "https://everynoise.com/everynoise1d.cgi?scope=mainstream%20only&vector=popularity"
# response = requests.get(url)
# html = BeautifulSoup(response.text, 'html.parser')
# genres = [re.sub("\d* ☊","",x.getText()) for x in html.find("body").findAll("tr")]
# print(genres[:10])
# with open("data/bandNameGenres.txt", "w+") as f:
#     f.writelines("\n".join(genres))

##city data from https://simplemaps.com/data/world-cities

