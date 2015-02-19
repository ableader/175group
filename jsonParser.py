# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 14:28:07 2015

@author: andrew
"""

import json
import pandas as pd
import matplotlib.pyplot as ply

tweets_data_path = 'twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
    
    # working from http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.html
    # http://adilmoujahid.com/posts/2014/07/twitter-analytics/
    #we are using tweepy (google tweepy)