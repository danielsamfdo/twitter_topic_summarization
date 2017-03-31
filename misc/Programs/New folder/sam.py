import tweepy
from tweepy import OAuthHandler
consumer_key="Twt0Fz9zpE9HpIjB8Ky3xQ"
consumer_secret="8rZlSDW7uOsBdtJAEjvbph3Oxy2UhJd9G43EpmsIU94"

access_token="143451652-hj6g5ehLyZEBJgi5IlBro7vYnNXvqIqGdUupxua2"
access_token_secret="1Gl0DkiZ93h4BsQ3xjQjJdhArBPInkbxJN3dZHsAxg"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's 
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
api.update_status('Up')
