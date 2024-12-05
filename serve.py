import requests
from starlette.requests import Request
from typing import Dict
from src.KeywordExtraction import KeywordExtractor
from src.JSONParser import JSONParser
from ray import serve

# 1: Wrap the pretrained sentiment analysis model in a Serve deployment.
@serve.deployment
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = KeywordExtractor()

    def __call__(self, request: Request) -> Dict:
        return self._model.keyword_extraction4(request.query_params["text"])


# 2: Deploy the deployment.
serve.run(SentimentAnalysisDeployment.bind(), route_prefix="/")

# 3: Query the deployment and print the result.

fp = "Data/data123.json"
parser = JSONParser()
parser.parse_json_file_with_path(fp)

return_val = requests.get(
        "http://localhost:8000/", params={"text": parser.large_string}
        ).json()

for item in return_val:
    print(item)
# {'label': 'POSITIVE', 'score': 0.9998476505279541}