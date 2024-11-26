import json
 
class JSONParser:
    def __init__(self):
        self.tweet_tuples = []
        self.large_string = ''

    def parse_json_file_with_path(self, path):
        '''Parses JSON files, adding them to a tweet tuple as normal,
        also adds them to a string
        Returns 1 on failure, 0 on success'''
        with open(path, 'r') as file:
            json_data = json.load(file)

        jsonposts = json_data["posts"]
        if jsonposts == None:
            print("ERROR: JSON does not contain posts")
            return 1
        
        for item in jsonposts:
            self.large_string += " " + item["record"]["text"]
            self.tweet_tuples.append((item["author"]["handle"], item["record"]["text"]))


    def parse_json_already_loaded(self, json):
        '''Parses a JSON, adding them to a tweet tuple as normal,
        also adds them to a string
        Returns 1 on failure, 0 on success'''

        jsonposts = json["posts"]
        if jsonposts == None:
            print("ERROR: JSON does not contain posts")
            return 1
        
        for item in jsonposts:
            self.large_string += " " + item["record"]["text"]
            self.tweet_tuples.append((item["author"]["handle"], item["record"]["text"]))