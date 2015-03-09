import json
import pandas as pd
import re
import numpy as np

tweets_input_path = 'twitter_table.csv'
word_map_input_path = 'word_map.txt'
companies = ['AAPL','AMZN','GOOG','MSFT']

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

#TODO interpret score based on stock trends
			
#Display results
#TODO format this properly
print(company_scores)
			
input("Hit return to continue")
