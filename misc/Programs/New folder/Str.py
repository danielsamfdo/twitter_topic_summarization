from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
ckey='RWKfuDvDNbwkCeBgzKUrSQ'
csecret='0kBYutOJp9U4k9ULVHzNqsG4gTqpXmdcKfKAGFh3QQ'
atoken='143451652-F0GmtWpNhFfvXsWu0NPyhL9mcT7w6jwvQeyeYHuj'
asecret='TRaTT7oswcgFzZJ649TOr5UXz5Y94YSV2B2vHV9dtYwGS'
class listener(StreamListener):
	def on_data(self,data):
		print(data)
		return True
	
	def on_error(self,status):
		print (status)

auth=OAuthHandler(ckey,csecret)
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')
session.set('request_token', (auth.request_token.key,auth.request_token.secret)
auth.set_access_token(atoken,asecret)

twitterStream=Stream("danielsamfdo","dan123",listener())
twitterStream.filter(track=["car"])
