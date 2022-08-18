import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import tweepy
    import schedule
    import time
    from datetime import date, datetime
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import random
    import sys
    import re
    import readline

def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

df = pd.read_csv("../data/ListBotData.csv").drop_duplicates("item")
old = df.iloc[df.used.values!=2,]
new = df.iloc[df.used.values==2,].reset_index(drop = True)
marked_for_deletion = []

print("Hello. There are " + str(new.shape[0]) + " new links today.")
for i in range(new.shape[0]):
    while 1:
        command = input("\nnew link #" + str(i+1) + ": " + new.item.values[i] + "\n(Ok/Edit/Delete): ")
        if command == "":
            print("Link approved.")
            break
        elif command.lower()[0] == "o":
            print("Link approved.")
            break
        elif command.lower()[0] == "d":
            print("Link deleted.")
            marked_for_deletion.append(i)
            break
        elif command.lower()[0] == "e":
            edited_link = rlinput("Please edit the link: ", new.item.values[i])
            new.item.values[i] = edited_link
            break
        else:
            print("Invalid command.")
    new.used.values[i] = 0
new = new.drop(index=marked_for_deletion)
pd.concat([old,new],axis=0).to_csv("../data/ListBotData.csv", index = False)

print("Goodbye.")
