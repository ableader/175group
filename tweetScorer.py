import json
import pandas as pd
import re
import numpy as np
import datetime
import pandas.io.data as web

tweets_input_path = 'twitter_table.csv'
word_map_input_path = 'word_map.txt'
companies = ['AAPL','AMZN','GOOG','MSFT']
start = datetime.datetime(2015, 2, 10)
end = datetime.datetime(2015, 2, 27)

#Load the tables
tweets = pd.read_csv(tweets_input_path)
with open(word_map_input_path) as infile:
    word_map = json.load(infile)

#Calculate the score of the tweets and add them to a score for a company
company_scores = {}
for company in companies:
	company_scores[company] = 0

for index, row in tweets.iterrows():
	tweet_score = 0
	#tweet scoring
	for w in row['text'].split(" "):
		word = w.lower()
		if word in word_map:
			tweet_score += word_map[word]
	#add score to applicable company
	for company in companies:
		if row[company]:
			company_scores[company] += tweet_score

#grab stock data from specified source
stock_dict = {}
for company in companies:
	stock_dict[company] = web.DataReader(company, 'google', start, end)
	#TODO compare stock data to score (get stock difference in start and end data and compare it to score)
	start_score = stock_dict[company].ix[start.date().isoformat()]['Close']
	end_score = stock_dict[company].ix[end.date().isoformat()]['Close']
	difference = end_score - start_score
	
#TODO use difference
#TODO catch the error that pops up if there is for some reason no stock data at the given start/end date
			
#Display results
#TODO format this properly
print(company_scores)
			
input("Hit return to continue")
