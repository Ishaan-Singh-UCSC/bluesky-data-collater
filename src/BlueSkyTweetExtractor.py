'''Contains functions in order to extract tweets from BlueSky.
@Params: TODO
@Return: TODO'''

from atproto import Client
from math import floor

class BlueskyTweetExtractor:
    def __init__(self, email, password):
        self.client = Client()
        self.profile = self.client.login(email, password)
        print('Successfully logged in as:', self.profile.display_name)
        return

    def get_tweets(self, batchsize):
        '''Uses bluesky api to get tweets in iterations and batch sizes, moving a cursor to get new tweets.'''
        tweets = []
        num_iters = floor(batchsize/100)
        first_iter = batchsize % 100
        if first_iter == 0:
            apiAccessLoop(self.client, num_iters, tweets)
        else:
            data = self.client.get_timeline(limit=first_iter)
            feed = data.feed
            nextpage = data.cursor
            for tweet in feed:
                tweets.append((tweet.post.author.handle, tweet.post.record.text))
            apiAccessLoop(self.client, num_iters, tweets)

        return tweets


def apiAccessLoop(client, num_iters, tweets):
    for i in range(num_iters):
        data = client.get_timeline(cursor=nextpage,limit=100)
        feed = data.feed
        nextpage = data.cursor
        for tweet in feed:
            tweets.append((tweet.post.author.handle, tweet.post.record.text))