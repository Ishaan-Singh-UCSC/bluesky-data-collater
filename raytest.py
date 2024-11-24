import ray
from atproto import Client, client_utils
import time
from random import randint

client = Client()
profile = client.login('ishnicucsc@gmail.com', 'ishaannicholasucsc')
print('Welcome,', profile.display_name)

DATA_CURSOR = '...'

@ray.remote
def get_tweets(iterations = 3, batchsize = 5):
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
        time.sleep(randint(1000,3000)/1000) 

    return

def main():
    data = ray.get(get_tweets.remote())
    for tweet in data:
        print(f"{tweet[0]}\n{tweet[1]}\n\n")

if __name__ == '__main__':
    main()