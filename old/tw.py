# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 21:39:01 2018

@author: Mag
"""

import tweepy
import pandas as pd
import re
import pickle
import matplotlib.pyplot as plt
from tweepy import OAuthHandler

# Please change with your own consumer key, consumer secret, access token and access secret
# Initializing the keys
consumer_key = 'rsjfIRKOedH8ulFELbvBRjnEG'
consumer_secret = '8fqPTctZCJO7ciKVz6KEWyzxRr111AZrU4lUXhozkK6koT7amW' 
access_token = '986923523003305984-tqdGEbO6SJfFJbnGgETtrYFkHCbKRwK'
access_secret ='bhxDnH0UHviirbGnnZW38sY1KCFoehmZnhpfUcWQtKPcI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

#api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
    
    
# jeden tweet    
a = public_tweets[0]

dir(a)
a.coordinates
a.author['location']
a._json
dir(a.user)
a.user.location
a.full_text

### pełny tekst tweeta

#    tweet_mode='extended'
public_tweets = api.home_timeline(tweet_mode='extended')
for tweet in public_tweets:
    print(tweet.full_text)
    print(tweet.user.location)
    
    # full_text zamiast text
    
b = public_tweets[0]
b.full_text
dir(b)

dir(b)

##########################################################################
######## WYSZUKIWANIE

###  -filter:retweets'

b = api.search('hackaton -filter:retweets', lang='pl', rpp=100, tweet_mode='extended')
b.count

for tweet in b:
    print(tweet.full_text)
    

##### kursor 
    
t = tweepy.Cursor(api.search,q='knf -filter:retweets',lang='pl', tweet_mode='extended').items(300)

for tw in t:
    print(tw.full_text)
    
t = tweepy.Cursor(api.search,q='knf -filter:retweets',lang='pl', tweet_mode='extended').items(5000)
tw_df=pd.DataFrame(columns=['tw_text', 'tw_loc'])

i=0

for tw in t:
    tw_df=tw_df.append(pd.DataFrame([[tw.full_text , tw.user.location]], columns=['tw_text', 'tw_loc']))
    i+=1
    if i % 100 ==0:
        print(i)
    
t[0]    
