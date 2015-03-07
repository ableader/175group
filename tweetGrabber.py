import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# get twitter keys from https://apps.twitter.com/app/7939294/keys
# Variables that contain user credentials
consumer_key = "5Uf3YjP5lY3t2MKHqxT87MLQf"
consumer_secret = "xeQ67UpvE8Fbq9MC3ThX00QJodCpfb8gVbOk0MY3nbmi1Loqj9"
access_token = "3024465769-YfhrWdXbNK33W88DZgi5yw8nMzLi2Ozog9dvvFM"
access_token_secret = "w28kDMBz8HKlnmtnNXqmh3GC8rbIAlSzuQAcRyGDwAJMi"

outputFile = "twitter_data.txt"
companies = ['AAPL','AMZN','GOOG','MSFT'] #List of companies to look through

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        dataFile = open(outputFile, 'w')
        dataFile.write(data)
        dataFile.close()
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
	
	#Assemble the hashtag list
	#Make sure there is a corresponding text file for each company (e.g. if apple is a company, there must be an apple.txt file)
	hashtag_list = []
	for company in companies:
		try:
			file_path = company + ('.txt')
			print(file_path)
			hashtag_file = open(file_path, "r")
			for line in hashtag_file:
				hashtag_list.append(line)
		except:
			print("derp")

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=hashtag_list)
