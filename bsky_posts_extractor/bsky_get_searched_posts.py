import requests
from typing import Dict, Any

def bsky_searched_posts(
        auth_token: str,
        url: str,
        search_phrase: str,
        required_posts: int,
) -> Dict[str, Any] :
    """
    Function that uses the `app.bsky.feed.searchPosts` endpoint in order to find all posts containing a certain phrase in any form.\n
    Works by iteratively searching until the number of required posts is found

    Args:
        auth_token (str): The `accessJwt` given through the auth endpoint
        url (str): The URL
        search_phrase (str): The phrase that this function will search for
        required_posts (int): The number of posts the function should find (works for any number >= 0)
    
    Returns:
        (Dict[str, Any]): A dictionary containing the searched posts data
    """
    consolidated_dict: Dict[str, Any] = {
        "posts": [],
        "cursor": 0
    } 
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {auth_token}"
    }
    limit: int = 100
    cursor: int = 0

    while True:
        if required_posts - cursor <= 0:
            break

        limit = min(100, required_posts - cursor)
        query_params: Dict[str, Any] = {
            "q": search_phrase,
            "limit": limit,
            "cursor": cursor
        }

        response = requests.get(
            url = url,
            headers = headers,
            params = query_params
        )
        
        response_json: Dict[str, Any] = response.json()
        cursor = int(response_json['cursor'])

        consolidated_dict['posts'].extend(response_json['posts'])
        consolidated_dict['cursor'] = cursor
    
    return consolidated_dict
