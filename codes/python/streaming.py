from slistener import SListener
import time, tweepy, sys

## auth. 
## TK: Edit the username and password fields to authenticate from Twitter.
#username = ''
#password = ''
#auth     = tweepy.auth.BasicAuthHandler(username, password)
#api      = tweepy.API(auth)

## Eventually you'll need to use OAuth. Here's the code for it here.
## You can learn more about OAuth here: https://dev.twitter.com/docs/auth/oauth
consumer_key        = "RWKfuDvDNbwkCeBgzKUrSQ"
consumer_secret     = "0kBYutOJp9U4k9ULVHzNqsG4gTqpXmdcKfKAGFh3QQ"
access_token        = "143451652-F0GmtWpNhFfvXsWu0NPyhL9mcT7w6jwvQeyeYHuj"
access_token_secret = "TRaTT7oswcgFzZJ649TOr5UXz5Y94YSV2B2vHV9dtYwGS"

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api      = tweepy.API(auth)
def main( mode = 1 ):
    track  = ['bjp']
    follow = []
            
    listen = SListener(api, 'test')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started on %s users and %s keywords..." % (len(track), len(follow))

    try: 
        stream.filter(track = track, follow = follow)
        #stream.sample()
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()
