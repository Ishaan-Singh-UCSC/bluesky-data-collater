from src.BlueSkyTweetExtractor import BlueskyTweetExtractor
from src.Tokenizer import BlueSkyTokenizer

NUM_TWEETS = 10

def main():
    creds = open("creds.txt", "r") 
    line = creds.readline()
    user_pass = line.split(",")
    creds.close()

    newExtractor = BlueskyTweetExtractor(user_pass[0], user_pass[1])

    data = newExtractor.get_tweets(NUM_TWEETS)
    for item in data:
        print(item,"\n")

    newTokenizer = BlueSkyTokenizer()
    tokenized_data = newTokenizer.convertToTokens_User_Tweet_Tuple(data)
    for item in tokenized_data:
        print(item, "\n")
    



if __name__ == '__main__':
    main()