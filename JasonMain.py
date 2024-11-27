import json
from src.KeywordExtraction import KeywordExtractor
from src.BERTTextSummarization import TextSummarizer
from src.JSONParser import JSONParser
#from bsky_posts_extractor.bsky_get_data import BskyData
import timeit
import os

def main():
        
    # fp = "Data/searchData.json"
    # with open(fp, 'r') as file:
    #     json_data = json.load(file)
    # parser = JSONParser()
    # parser.parse_json_already_loaded(json_data)


    # jsonposts = json_data["posts"]
    # if jsonposts == None:
    #     print("ERROR: JSON does not contain posts")
    #     exit()
    # data_string = ''

    # for item in jsonposts:
    #     data_string += " " + item["record"]["text"]
    # obj = BskyData(
    #     required_posts=1000,
    #     search_phrase="League of Legends"
    # )

    fp = "Data/data.json"
    parser = JSONParser()
    parser.parse_json_file_with_path(fp)
    with open(fp, 'r') as file:
            json_data = json.load(file)
    i = 0
    for item in json_data["posts"]:
        i += 1
    print("NUM POSTS:", i)
    start = timeit.default_timer()
    newKeywordExtractor = KeywordExtractor()
    keywords = newKeywordExtractor.keyword_extraction(parser.large_string)
    keywords2 = newKeywordExtractor.keyword_extraction2(parser.large_string)
    keywords3 = newKeywordExtractor.keyword_extraction3(parser.large_string)
    keywords4 = newKeywordExtractor.keyword_extraction4(parser.large_string)
   
    end = timeit.default_timer()
    print(f"time taken: {end - start}")
    print("keywords 1:")
    for item in keywords:
        print (item)
    print("\nkeywords 2:")
    for item in keywords2:
        print(item)

    print("\nkeywords 3:")
    for item in keywords3:
        print(item)

    print("\nkeywords 4:")
    for item in keywords4:
        print(item)

    # print("\nkeywords 5:")
    # for item in keywords5:
    #     print(item)


    newSummarizer = TextSummarizer()
    summary = newSummarizer.summarizeString(parser.large_string)
    print("Summary:", summary)
    
    

if __name__ == '__main__':
    main()
