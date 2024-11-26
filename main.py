from src.BlueSkyTweetExtractor import BlueskyTweetExtractor
# from src.Tokenizer import BlueSkyTokenizer
# from src.BERTTextSummarization import TextSummarizer
from src.KeywordExtraction import KeywordExtractor

# Number of tweets to find
NUM_TWEETS = 1000
NUMCORES = 1
def main():
    '''Gets tweets from Bluesky based on a set variable, and finds the keywords to print'''
    print("Getting", NUM_TWEETS, "tweets")
    creds = open("creds2.txt", "r") 
    line = creds.readline()
    user_pass = line.split(",")
    creds.close()

    newExtractor = BlueskyTweetExtractor(user_pass[0], user_pass[1])

    data = newExtractor.get_tweets(NUM_TWEETS)
    string_data = ''
    for item in data:
        string_data += " " + item[1]
        # print(item,"\n")
    
    newKeywordExtractor = KeywordExtractor()
    keywords = newKeywordExtractor.keyword_extraction(string_data)
    keywords2 = newKeywordExtractor.keyword_extraction2(string_data)
    for item in keywords:
        print (item)
    for item in keywords2:
        print(item)
    
    # print("Found tweets: ", len(data))
    # Tokenizer, not used
    # newTokenizer = BlueSkyTokenizer()
    # tokenized_data = newTokenizer.convertToTokens_User_Tweet_Tuple(data)
    # for item in tokenized_data:
    #     print(item, "\n")
    
    # Summarizer, not used
    # newSummarizer = TextSummarizer()
    # summaries = newSummarizer.summarize_Tweets(data, NUMCORES)

if __name__ == '__main__':
    main()