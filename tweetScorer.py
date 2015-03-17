import json
import pandas as pd
import re
import numpy as np
import datetime
import pandas.io.data as web

tweets_input_path = 'twitter_table.csv'
word_map_input_path = 'word_map.txt'
weight_map_output_path = 'weight_map.txt'
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

#grab stock data from specified date and compare
weight_map = {}
for company in companies:
	stock_data = web.DataReader(company, 'google', start, end)
	start_score = stock_data.ix[start.date().isoformat()]['Close']
	end_score = stock_data.ix[end.date().isoformat()]['Close']
	difference = end_score - start_score
	weight_map[company] = company_scores[company]/difference
		
#Save weight map
with open(weight_map_output_path, 'w') as outfile:
    json.dump(weight_map, outfile)
			
input("Hit return to continue")
