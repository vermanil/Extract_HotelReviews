import tweepy
consumer_key= 'QVudSTJo7kvR0UGrlI5FmOQz8'
consumer_secret= 'CHLcbmM9k6eWKNddX7OOsY6ChaeMP4rtGbTuNYmKGcOGanVWSh'
access_token='865442933842956289-Bwt1ZPyUmMKh5QotQwTzLFCRmuMRf9i'
access_token_secret='lXSQOzs5DtjakBNgFpDrliDVxIUBFWUHJjCcPyQlkIOos'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

arr = ['oyo room','good']

public_tweets = api.search(arr)
# print public_tweets.text
print len(public_tweets)
for tw in public_tweets:
	print tw.text