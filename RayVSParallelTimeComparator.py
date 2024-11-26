import ray
from atproto import Client, client_utils
from random import randint
import timeit
import os
import math

NUM_CPUS = 4
client = Client()
profile = client.login('ishnicucsc@gmail.com', '###')
print('Welcome,', profile.display_name)


def get_tweets(batchsize):
    '''Uses bluesky api to get tweets in iterations and batch sizes, moving a cursor to get new tweets.'''
    tweets = []
    num_iters = math.floor(batchsize/100)
    first_iter = batchsize % 100
    data = client.get_timeline(limit=first_iter)
    feed = data.feed
    nextpage = data.cursor
    for tweet in feed:
        tweets.append((tweet.post.author.handle, tweet.post.record.text))
    
    for i in range(num_iters):
        data = client.get_timeline(cursor=nextpage,limit=100)
        feed = data.feed
        nextpage = data.cursor
        for tweet in feed:
            tweets.append((tweet.post.author.handle, tweet.post.record.text))
    return tweets

BATCH_SIZES = [1525, 1675, 1825, 1975, 2125, 2275, 2425, 2575, 2725, 2875, 3025, 3175, 3325, 3475, 3625, 3775, 3925, 4075, 4225, 4375, 4525, 4675, 4825, 4975]

def map_normal(data, NUM_CPUS):
    mapped_data=[]
    for i in range(NUM_CPUS):
        mapped_data.append([])
    i = 0
    for item in data:
        mapped_data[i%NUM_CPUS].append(item)
        i += 1
    return mapped_data

@ray.remote
def map_remote(data, arraynum, datalen, NUM_CPUS):
    mapped_data = []
    i = arraynum
    while i < datalen:
        mapped_data.append(data[i])
        i += NUM_CPUS
    return mapped_data


# BATCH_SIZES = [50, 125, 175, 225, 275, 325, 375, 425, 475, 525, 575, 625, 675, 725, 775, 825, 875, 925, 975, 1025, 1075]
NUM_CPUS = 16
NUM_TWEETS = 4975
data = get_tweets(NUM_TWEETS)

path = "Data/timer_test.csv"
f = open(path,'w')
for batch in BATCH_SIZES:
    #remote funciton
    batched_data = data[0:batch]
    length = len(batched_data)
    print("len:", length)
    for i in range(3):
        startRemote = timeit.default_timer()
        data_list = [map_remote.remote(batched_data, x, length, NUM_CPUS) for x in range(NUM_CPUS)]
        ray.wait(data_list)
        ray.get(data_list) 
        endRemote = timeit.default_timer()


        startParallel = timeit.default_timer()
        mapped_data2 = map_normal(batched_data, NUM_CPUS)
        endParallel = timeit.default_timer()

        print(f"{length},{endRemote-startRemote},{endParallel - startParallel}", file=f)