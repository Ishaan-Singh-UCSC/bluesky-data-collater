import ray
from atproto import Client, client_utils
import time
from random import randint
NUM_CPUS = 4

client = Client()
profile = client.login('ishnicucsc@gmail.com', 'ishaannicholasucsc')
print('Welcome,', profile.display_name)

DATA_CURSOR = '...'

def get_tweets(iterations = 3, batchsize = 50):
    data = client.get_timeline()

    # for now, cap iterations TODO: remove this cap
    iters = 3 
    # iters = iterations

    # TODO: for now, cap posts per
    posts_per = 5
    # if batchsize < 1 or batchsize > 100:
    #     posts_per = 50
    # else:
    #     posts_per = batchsize

    for i in range(iters):
        # Waits between 1-3 seconds to send next data
        client.get_timeline(cursor=DATA_CURSOR, limit=posts_per)

        
        # Returns both the author and the tweet
        for tweet in data:
            yield (tweet.post.author.handle, tweet.post.record.text)
    return

@ray.remote
def map_(data, arraynum):
    mapped_data = []
    i = 0
    for item in data:
        if (i % 4) == arraynum:
            mapped_data.append(item)
    return mapped_data

@ray.remote
def bert_thing():
    # TODO: make this function.
    return


def main():
    ray.init(num_cpus=NUM_CPUS)
    data = get_tweets.remote()

    mapped_data = [map_.remote(data, i) for i in range(NUM_CPUS)]
    results = 
    

if __name__ == '__main__':
    main()