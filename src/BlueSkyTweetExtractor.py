from atproto import Client
from math import floor

class BlueskyTweetExtractor:
    '''Use this class to extract tweets from bluesky'''
    def __init__(self, email, password):
        '''Creates the BlueskyTweetExtractor object, usuing atproto api.
        Takes an email and password to login'''
        self.client = Client()
        self.profile = self.client.login(email, password)
        print('Successfully logged in as:', self.profile.display_name)

    def get_tweets(self, batchsize=10):
        '''Uses bluesky api to get tweets in iterations and batch sizes, moving a cursor to get new tweets.
        Takes a batchsize int. Return in the form of a list of tuples ("{Posting User}", "{Tweet content}")'''
        tweets = []
        # Invalid input will return 10 tweets
        if batchsize < 1:
            batchsize = 10
        # Max limit size is 100, so it determines how many to take
        num_iters = floor(batchsize/100)
        first_iter = batchsize % 100

        # These two blocks will loop through and get the desired amount of tweets according to batchsize
        # When the amount of tweets to get is divisible by 100
        if first_iter == 0:
            # Retreives the data of all the tweets
            data = self.client.get_timeline(limit=100)
            # Generator object for all the tweets found
            feed = data.feed
            # Nextpage tracks where to start when we continue to gather tweets
            nextpage = data.cursor
            # Extracts data in a loop
            for tweet in feed:
                # Removes reply tweets
                #if tweet.post.record.reply == None: 
                tweets.append((tweet.post.author.handle, tweet.post.record.text))
            __apiAccessLoop__(self.client, num_iters - 1, tweets, nextpage)
        # When the amount of tweets to get is not divisible by 100
        else:
            data = self.client.get_timeline(limit=first_iter)
            feed = data.feed
            nextpage = data.cursor
            for tweet in feed:
                # Removes reply tweets
                # if tweet.post.record.reply == None:
                tweets.append((tweet.post.author.handle, tweet.post.record.text))
            __apiAccessLoop__(self.client, num_iters, tweets, nextpage)
        return tweets
    
    def get_training_tweets(self):
        tweets = []
        data = self.client.get_profile(actor='did:plc:l37rmaqsv54sahg54owqfwmy')
        did = data.did
        display_name = data.display_name
        print("Retrieving profile for: ", data.display_name)
        # TODO
        print("TODO")
        return tweets


def __apiAccessLoop__(client, num_iters, tweets, nextpage):
    '''Loop of repeating code to simplify process. not meant to be called by the user'''
    for i in range(num_iters):
        data = client.get_timeline(cursor=nextpage,limit=100)
        feed = data.feed
        nextpage = data.cursor
        for tweet in feed:
            # Removes reply tweets
            if tweet.post.record.reply == None:
                tweets.append((tweet.post.author.handle, tweet.post.record.text))