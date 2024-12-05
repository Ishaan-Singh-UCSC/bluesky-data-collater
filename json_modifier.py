import json
from typing import Any

def parse_json(
        input_json_fp: str, 
        output_json_fp: str,
        label: int = 1
    ) -> None:
    '''
    Gets data from the input JSON, parses it, and then prints it to the output JSON

    Args:
        input_json_fp (str): The filepath of the input JSON
        output_json_fp (str): The filepath of the output JSON
        label (str): The label value for the output JSON, set to 1 by default
    
    Returns:
        None
    '''

    with open(input_json_fp, 'r') as input_file:
        input_data = json.load(input_file)

    all_posts: list[dict[str, Any]] = input_data['posts']
    output_json: list[dict[str, Any]] = list()

    for post in all_posts:
        # The location where the text is stored in the JSON file
        post_text: str = post['record']['text']
        output_json.append({
            'text': post_text,
            'label': label
            
        })
    
    with open(output_json_fp, 'w') as output_file:
        json.dump(
            obj = output_json,
            fp = output_file,
            indent = 4,
        )
        

if __name__ == '__main__':
    import os

    input_fp = os.path.dirname(__file__) + "/Data/data123.json"
    output_fp = os.path.dirname(__file__) + "/data_train.json"

    parse_json(
        input_json_fp = input_fp,
        output_json_fp = output_fp
    )

