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


t = tweepy.Cursor(api.search,q='knf -filter:retweets',lang='pl', tweet_mode='extended').items(1000)

pd_s = pd.Series(['' for i in range(1,1001)])

tw_df=pd.concat([pd_s, pd_s], axis=1)
tw_df.columns = ['tw_text', 'tw_location']


tw_df=pd.DataFrame(columns=['tw_text', 'tw_loc'])


i=0
time_start = datetime.datetime.now()
for tw in t:
    tw_df=tw_df.append(pd.DataFrame([[tw.full_text , tw.user.location]], columns=['tw_text', 'tw_loc']))
    i+=1
    if i % 100 ==0:
        print(i, " at ", datetime.datetime.now())
        

time_stop = datetime.datetime.now()
print('Total time: ', time_stop-time_start)
#Total time:  0:00:31.826828

## inaczej
i=0
time_start = datetime.datetime.now()
for tw in t:
    tw_df.iloc[i][0]=tw.full_text
    tw_df.iloc[i][1]=tw.user.location
    i+=1
    if i % 100 ==0:
        print(i, " at ", datetime.datetime.now())
        

time_stop = datetime.datetime.now()
print('Total time: ', time_stop-time_start)
#Total time:  0:00:27.975456



with open('tweets.pickle','wb') as f:
                pickle.dump(tw_df,f)


#Total time:  0:00:23.923916





t = tweepy.Cursor(api.search,q='knf -filter:retweets',lang='pl', tweet_mode='extended').items(1000)
tw_df=pd.DataFrame(columns=['tw_text', 'tw_loc'])

i=0
time_start = datetime.datetime.now()
for tw in t:
    tw_df=tw_df.append(pd.DataFrame([[tw.full_text , tw.user.location]], columns=['tw_text', 'tw_loc']))
    i+=1
    if i % 100 ==0:
        print(i, " at ", datetime.datetime.now())

time_stop = datetime.datetime.now()
print('Total time: ', time_stop-time_start)
#Total time:  0:00:25.897123