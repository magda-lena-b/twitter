# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 21:03:07 2018

@author: Mag
"""



import tweepy
import datetime
import pandas as pd
import re
import pickle
import matplotlib.pyplot as plt
from tweepy import OAuthHandler


# dane do autoryzacji
consumer_key, consumer_secret ,access_token, access_secret = list(pd.read_csv('tw_auth.csv', header=None)[0])

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit_notify = True, wait_on_rate_limit=True)


t = tweepy.Cursor(api.search,q='knf -filter:retweets',lang='pl', tweet_mode='extended').items(10)

#####################################
## dataframe na wyniki


tw_df = pd.DataFrame(index=range(10), columns=['tw_text', 'location', 'user_id', 'user_name', 'fav_cnt','friends_cnt', 'foll_cnt'])

#####################################
## ładowanie danych

i=0
time_start = datetime.datetime.now()
for tw in t:
    tw_df.iloc[i]=[tw.full_text, tw.user.location, tw.user.id, tw.user.name, tw.user.favourites_count, tw.user.friends_count, tw.user.followers_count]
    i+=1
    if i % 100 ==0:
        print(i, " at ", datetime.datetime.now())
    if i % 1000 ==0:
        with open('tweets.pickle','wb') as f:
                pickle.dump(tw_df,f)

print('Total time: ', datetime.datetime.now()-time_start)
#Total time:  0:31:13.995381



with open('tweets.pickle','wb') as f:
                pickle.dump(tw_df,f)


#Total time:  0:00:23.923916



#### testowanie info o lokalizacji
                
u = api.get_user(id=174228069)
dir(u)
u.favourites_count
