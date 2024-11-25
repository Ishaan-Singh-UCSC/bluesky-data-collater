import ray
from atproto import Client, client_utils
import time
from random import randint
import timeit

from transformers import BertTokenizer, BertForMaskedLM
import torch

NUM_CPUS = 4

client = Client()
profile = client.login('ishnicucsc@gmail.com', 'ishaannicholasucsc')
print('Welcome,', profile.display_name)

DATA_CURSOR = '...'


def get_tweets(iterations = 3, batchsize = 50):
    '''Uses bluesky api to get tweets in iterations and batch sizes, moving a cursor to get new tweets.'''
    data = client.get_timeline(limit=batchsize)
    feed = data.feed
    print("to find:", type(data))
    # for now, cap iterations TODO: remove this cap
    iters = 1
    # iters = iterations

    # TODO: for now, cap posts per
    posts_per = 10
    # if batchsize < 1 or batchsize > 100:
    #     posts_per = 50
    # else:
    #     posts_per = batchsize
    data_formatted = []
    for i in range(iters):
        # Waits between 1-3 seconds to send next data
        # client.get_timeline(limit=posts_per)
        # client.get_timeline(cursor=DATA_CURSOR, limit=posts_per)
        
        # Returns both the author and the tweet
        for tweet in feed:
            data_formatted.append((tweet.post.author.handle, tweet.post.record.text))
            #yield (tweet.post.author.handle, tweet.post.record.text)
    return data_formatted

@ray.remote
def map_remote(data, arraynum, datalen, NUM_CPUS):
    mapped_data = []
    i = arraynum
    while i < datalen:
        mapped_data.append(data[i])
        i += NUM_CPUS
    return mapped_data

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
def bert_thing():
    # TODO: make this function.
    return


def main():
    batchsize = 100
    ray.init(num_cpus=NUM_CPUS)
    data = get_tweets(batchsize=batchsize)
    data_len = len(data)

    #start = time.time()
    start1 = timeit.default_timer()
    mapped_data = []
    for i in range(NUM_CPUS):
        mapped_data.append(map_remote.remote(data, i, data_len, NUM_CPUS))
    end1 = timeit.default_timer()
    # mapped_data = [map_remote.remote(data, i, data_len, NUM_CPUS) for i in range(NUM_CPUS)]
    #end = time.time()

    start = timeit.default_timer()
    mapped_data2 = map_normal(data, NUM_CPUS)
    end = timeit.default_timer()
    print("batch, dist time, normal time")
    print(f"{batchsize},{end1-start1},{end - start}")

if __name__ == '__main__':
    main()