# StockGrabber.py
# Reads a pandas csv file that contains tabulated twitter data and assigns values based on corresponding stock values
#
#

import json
import pandas as pd
import re
import datetime
import pandas.io.data as web

tweets_input_path = 'twitter_table.csv'
word_map_output_path = 'word_map.txt'
companies = ['AAPL','AMZN','GOOG','MSFT']
start = datetime.datetime(2015, 2, 1)
end = datetime.datetime(2015, 2, 27)


#Load pandas table
tweets = pd.read_csv(tweets_input_path)

#Read stock data
stock_dict = {}
for company in companies:
	stock_dict[company] = web.DataReader(company, 'google', start, end)

#Map stocks to pandas table entries based on date and company
#Example date string: "Tue Jul 15 14:19:30 +0000 2014"
wordlist_dict = {}
for index, row in tweets.iterrows():
	dt_list = row['created_at'].split()
	dt_str = dt_list[5] + ' ' + dt_list[1] + ' ' + dt_list[2]
	dt = datetime.datetime.strptime(dt_str, "%Y %b %d").date()
	#Assign value to the tweet
	hits = 0
	val = 0
	for company in companies:
		if row[company]:
			stock_info = stock_dict[company].ix[dt.isoformat()]
			val += stock_info['Close']
			hits += 1
	if hits > 0:
		val /= hits
	#Add tweet's value to word's list of values (set everything to lowercase)
	for w in row['text'].split(" "):
		word = w.lower()
		if word in wordlist_dict:
			wordlist_dict[word].append(val)
		else:
			wordlist_dict[word] = [val]
	
#Create word map
#Value of a word is the average of the values in its list multiplied by a factor of its frequency
#TODO frequency multiplier is determined by the word with the most tweets
wordavg_dict = {}
for word in wordlist_dict:
	#wordavg_dict[word] = sum(wordlist_dict[word]) / len(wordlist_dict[word])
	wordavg_dict[word] = sum(wordlist_dict[word]) / len(max(wordlist_dict,key=len))
	
#Save the word dict
with open(word_map_output_path, 'w') as outfile:
    json.dump(wordavg_dict, outfile)
	
input("Hit return to continue")
