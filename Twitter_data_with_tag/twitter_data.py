import tweepy
consumer_key= 'Add your consumer Key'
consumer_secret= 'Add consumer Secret Key'
access_token='Add access token'
access_token_secret='add access secret token'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

sentence = raw_input("Enter your tag u want to search")
arr = sentence.split(" ")
# arr = ['oyo room','good']

public_tweets = api.search(arr)
# print public_tweets.text
print len(public_tweets)
for tw in public_tweets:
	print tw.text