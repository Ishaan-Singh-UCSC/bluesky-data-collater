import json
from src.KeywordExtraction import KeywordExtractor
from src.BERTTextSummarization import TextSummarizer
from src.JSONParser import JSONParser

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

    fp = "Data/searchData.json"
    parser = JSONParser()
    parser.parse_json_file_with_path(fp)

    newKeywordExtractor = KeywordExtractor()
    keywords = newKeywordExtractor.keyword_extraction(parser.large_string)
    keywords2 = newKeywordExtractor.keyword_extraction2(parser.large_string)
    keywords3 = newKeywordExtractor.keyword_extraction3(parser.large_string)
    print("keywords 1:")
    for item in keywords:
        print (item)
    print("\nkeywords 2:")
    for item in keywords2:
        print(item)

    print("\nkeywords 3:")
    for item in keywords3:
        print(item)

    newSummarizer = TextSummarizer()
    summary = newSummarizer.summarizeString(parser.large_string)
    print("Summary:", summary)
    
    

if __name__ == '__main__':
    main()