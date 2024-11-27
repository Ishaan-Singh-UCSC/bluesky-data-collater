import json, os
from src.KeywordExtraction import KeywordExtractor
from src.JSONParser import JSONParser
from bsky_posts_extractor.bsky_get_data import BskyData
import ray
import timeit

NUMCPUS=8

def main():
    obj = BskyData(
        required_posts=1000,
        search_phrase="League of Legends"
    )
    fp = os.path.dirname(__file__) + "/Data/data.json"
    parser = JSONParser()
    parser.initialize_ray_parser(NUMCPUS)
    parser.ray_parser_path(fp)
    

    newKeywordExtractor = KeywordExtractor()



    
    start = timeit.default_timer()
    keywords = [keyword_extractor_machine.remote(parser.string_array[i]) for i in range(NUMCPUS)]
    #keywords1 = keyword_extractor_machine.remote(parser.string_array[0])
    #keywords2 = keyword_extractor_machine.remote(parser.string_array[1])

    #ray.get(keywords1)
    #ray.get(keywords2)
    ray.get(keywords)
    end = timeit.default_timer()


    print(f"time taken: {end - start}")
    # print(type(keywords1))
    # print("keywords 1:")
    # for item in keywords1[0]:
    #     print (item)
    # print("\nsecond_second_keywords 1:")
    # for item in keywords2[1]:
    #     print (item)


    # print("\n\n\n\nkeywords 2:")
    # for item in keywords1[0]:
    #     print(item)
    # print("\nsecond_keywords 2:")
    # for item in keywords2[1]:
    #     print(item)


    # print("\n\n\n\nkeywords 3:")
    # for item in keywords1[0]:
    #     print(item)
    # print("\nsecond_keywords 3:")
    # for item in keywords2[1]:
    #     print(item)

    # print("\n\n\n\nkeywords 4:")
    # for item in keywords1[0]:
    #     print(item)
    # print("\nsecond_keywords 4:")
    # for item in keywords2[1]:
    #     print(item)


@ray.remote
def keyword_extractor_machine(string_array):
    newKeywordExtractor = KeywordExtractor()
    return_data = []
    return_data.append(newKeywordExtractor.keyword_extraction(string_array))
    return_data.append(newKeywordExtractor.keyword_extraction2(string_array))
    return_data.append(newKeywordExtractor.keyword_extraction3(string_array))
    return_data.append(newKeywordExtractor.keyword_extraction4(string_array))
    return return_data

if __name__ == '__main__':
    main()
