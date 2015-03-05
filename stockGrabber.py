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
tweets_output_path = 'twitter_table_formatted.csv'
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
#TODO stock vals might not be necessary
stock_vals = []
for index, row in tweets.iterrows():
	dt_list = row['created_at'].split()
	dt_str = dt_list[5] + ' ' + dt_list[1] + ' ' + dt_list[2]
	dt = datetime.datetime.strptime(dt_str, "%Y %b %d").date()
	#TODO stock mapping
	hits = 0
	val = 0
	for company in companies:
		if row[company]:
			stock_info = stock_dict[company].ix[dt.isoformat()]
			val += stock_info['Close'] #TODO is this right
			hits += 1
	if hits > 0:
		val /= hits
	stock_vals.append(val)
	#TODO possibly do word map creation in this loop
tweets['value'] = stock_vals
	
#TODO create word map	
	
#Save the new pandas table TODO this might not be necessary
tweets.to_csv(tweets_output_path)
	
input("Hit return to continue")
