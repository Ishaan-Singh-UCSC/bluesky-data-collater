from src.BlueSkyTweetExtractor import BlueskyTweetExtractor

creds = open("creds.txt", "r") 
line = creds.readline()
user_pass = line.split(",")
creds.close()

newExtractor = BlueskyTweetExtractor(user_pass[0], user_pass[1])

print(newExtractor.get_tweets(30))