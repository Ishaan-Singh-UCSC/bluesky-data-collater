import json
from src.KeywordExtraction import KeywordExtractor
from src.BERTTextSummarization import TextSummarizer

def main():
        
    fp = "Data/searchData.json"
    with open(fp, 'r') as file:
        json_data = json.load(file)

    jsonposts = json_data["posts"]
    if jsonposts == None:
        print("ERROR: JSON does not contain posts")
        exit()
    data_string = ''

    for item in jsonposts:
        data_string += " " + item["record"]["text"]

    newKeywordExtractor = KeywordExtractor()
    keywords = newKeywordExtractor.keyword_extraction(data_string)
    keywords2 = newKeywordExtractor.keyword_extraction2(data_string)
    keywords3 = newKeywordExtractor.keyword_extraction3(data_string)
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
    summary = newSummarizer.summarizeString(data_string)
    print("Summary:", summary)
    
    

if __name__ == '__main__':
    main()