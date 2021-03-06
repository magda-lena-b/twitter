# -*- coding: utf-8 -*-
"""
Created on F Nov 30 21:03:07 2018

@author: Mag
"""
import pickle
import tweepy
import datetime
import pandas as pd
import requests
import re
import geopandas as gpd
import matplotlib as plt


def set_api(auth_file):
    """ returns api """
    
    consumer_key, consumer_secret ,access_token, access_secret = list(pd.read_csv(auth_file, header=None)[0])
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    return tweepy.API(auth, wait_on_rate_limit_notify = True, wait_on_rate_limit=True)






def load_tweets(api, query = " ", number= 100, with_loc = 1):
    """ downloads given number of tweets with given subject """
    
    """
    api - tweepy.API
    query - string to search
    number - maximum number of tweets to download
    with_loc - when set to 1 will omitt tweets without author's location or with one that is listed in bad_locs list
    
    """
    
    t = tweepy.Cursor(api.search,q=query+' -filter:retweets',lang='pl', tweet_mode='extended').items(number)
    
    # results dataframe
    tw_df = pd.DataFrame(index=range(number), columns=['tw_text', 'location', 'user_id', 'user_name', 'fav_cnt','friends_cnt', 'foll_cnt'])
    
    #  checks location for reasnable inputs
    bad_locs = ['', 'polska', 'poland','europe', 'europa', 'azja', 'asia', 'usa']
    i=0
    time_start = datetime.datetime.now()
    
    for tw in t:
        if (tw.user.location.lower() in bad_locs and with_loc==1):
            pass
        else:
            tw_df.iloc[i]=[tw.full_text, tw.user.location, tw.user.id, tw.user.name, tw.user.favourites_count, tw.user.friends_count, tw.user.followers_count]
        i+=1
        if i % 500 ==0:
            print(i, " at ", datetime.datetime.now())

    #   dumps a pickle        
    tw_df = tw_df[tw_df['location']!=''].dropna()
    with open(query+'_tweets.pickle','wb') as f:
        pickle.dump(tw_df,f)
    
    if with_loc==1:
        r = ' with author\'s location'
    else:
        r=''
        
    print('Got {} tweets about "{}{}'.format(len(tw_df), query, r))
    print('Total time: ', datetime.datetime.now()-time_start)
    return tw_df






def get_state(location):
    """ gets state info for location from openstreetmap"""
    #print(location)
    location = re.sub('\W', ' ',location)
    conf = {'format': 'json', 'addressdetails': 1, 'limit' : 1, 'q': location}
    loc_data = requests.get('http://nominatim.openstreetmap.org', params=conf).json()
    if ((len(loc_data)==0) & (len(location.split())>0)):
        conf = {'format': 'json', 'addressdetails': 1, 'limit' : 1, 'q': location.split()[0]}
        loc_data = requests.get('http://nominatim.openstreetmap.org', params=conf).json()
            
        if len(loc_data)==0:
            print('Couldn\'t get location for {}'.format(location))
            return None

    try:
        state = loc_data[0]['address']['state']
    except KeyError:
        print('Location "{}" doesn\'t have a state value'.format(location))
        return None
    except IndexError:
        print('Couldn\'t get location for {}'.format(location))
        return None
    
    return state



def basic_map(plot_data, column, title='', cmap = 'Blues'):
    """ very simple map plotting """
    assert(isinstance(plot_data, gpd.GeoDataFrame)), "Data needs to be a GeoDataFrame"
    fig, ax = plt.subplots(1, figsize=(8, 8))
    plot_data.plot(ax = ax, linewidth=0.5, edgecolor='0.4', column=column, cmap=cmap, legend=True, scheme='quantiles')
    ax.set_title(title, fontdict={'fontsize': 20}, loc='left')
    ax.get_legend().set_bbox_to_anchor((.2, .3))
    ax.axis('off')
    
#ap = set_api('tw_auth.csv')
#all_t = load_tweets(ap, ' ', 10000)
