import requests, os, sys
from starlette.requests import Request
from typing import Dict
from ray import serve

# this adds src to the absolute path ensuring that there's no issues with importing it into this file
# added because there was an error that wasn't recognizing src as a valid package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.KeywordExtraction import KeywordExtractor
from src.JSONParser import JSONParser
from bsky_posts_extractor.bsky_get_data import BskyData


# 1: Wrap the pretrained sentiment analysis model in a Serve deployment.
@serve.deployment
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = KeywordExtractor()

    def __call__(self, request: Request) -> Dict:
        return self._model.keyword_extraction4(request.query_params["text"])



if __name__ == '__main__':

    num_required_posts = 1000
    search_phrase = "Spotify"

    input_fp = os.path.dirname(__file__) + "/Data/data.json"
    output_fp = os.path.dirname(__file__) + "/ray_output.txt"

    # 2: Deploy the deployment.
    serve.run(SentimentAnalysisDeployment.bind(), route_prefix="/")

    # 3: Get the posts from BlueSky
    print(f"\nSearching for {num_required_posts} posts with the search phrase '{search_phrase}'\n")

    bsky_scraped_data = BskyData(
        required_posts = num_required_posts,
        search_phrase = search_phrase
    )

    print(f"Posts scraped!\n")
    
    parser = JSONParser()
    parser.parse_json_file_with_path(input_fp)

    # 4: Query the deployment and print the result.

    return_val = requests.get(
            "http://localhost:8000/", params={"text": parser.large_string}
            ).json()

    with open(output_fp, 'w', encoding='utf-8') as output_file:
        for item in return_val:
            output_file.write(str(item) + '\n')
        
    print(f"Run finished! Check {output_fp.split('/')[-1]} for the output!\n")
    # {'label': 'POSITIVE', 'score': 0.9998476505279541}

