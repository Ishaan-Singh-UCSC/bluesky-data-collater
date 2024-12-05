
from typing import Dict, Any
import os, json

import requests
from typing import Dict, Any
import json, os


def get_auth_token(
        url: str,
        identifier: str,
        password: str
) -> Dict[str, Any]:
    """
    Function to the get the auth token from the BlueSky auth server

    Args:
        url (str): The endpoint being hit with a post request
        identifier (str): Either the handle or the email associated with the desired account
        password (str): The password associated with the account
    
    Returns:
        (Dict[str, Any]): Either the dictionary containing the data from the API, or an error message
    """
    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }
    payload: Dict[str, str] = {
        "identifier": identifier,
        "password": password
    }

    response = requests.post(
        url = url,
        headers = headers,
        json = payload
    )

    with open(os.path.dirname(__file__) + "/auth.json", 'w') as file:
        json.dump(response.json(), file, indent=4)

    if response.status_code == 200:
        response_json: Dict[str, Any] = response.json()
        return response_json
    else:
        err_json: Dict[str, Any] = {
            "error": response.status_code,
            "message": "An error has occurred"
        }
        return err_json

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

import requests
from typing import Dict, Any

def delete_session(
        url: str,
        refreshJwt: str
) -> bool:
    """
    Deletes the BlueSky session

    Args:
        url (str): The delete session url
        refreshJwt (str): The refresh JWT provided by BlueSky, required to delete session
    
    Returns:
        bool: True if 200 statuscode, False otherwise
    """
    headers: Dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {refreshJwt}"
    }

    response = requests.post(
        url = url,
        headers = headers
    )

    return response.status_code == 200

class BskyData:
    def __init__(
            self, 
            required_posts: int, 
            search_phrase: str, 
            input_username: str | None = None, 
            input_password: str | None = None
    ) -> None:
        output_filepath: str = os.path.dirname(__file__) + "/../Data/data.json"
        login_filepath: str = os.path.dirname(__file__) + "/password_data.json"
        auth_filepath: str = os.path.dirname(__file__) + "/auth.json"

        # login details
        with open(login_filepath, 'r') as file:
            login_data = json.load(file)
        
        

        username: str = input_username or login_data['username']
        password: str = input_password or login_data['password']

        delete_url: str = 'https://bsky.social/xrpc/com.atproto.server.deleteSession'
        auth_url: str = 'https://bsky.social/xrpc/com.atproto.server.createSession'
        posts_url: str = 'https://bsky.social/xrpc/app.bsky.feed.searchPosts'

        # deleting the session to restart if the file exists
        if os.path.exists(auth_filepath):
            with open(auth_filepath, 'r') as file:
                auth_data = json.load(file)

            refresh_jwt: str = auth_data['refreshJwt']

            session_deleted: bool = delete_session(
                url = delete_url,
                refreshJwt = refresh_jwt
            )

            if not session_deleted:
                raise Exception("Something went wrong with deletion of session, please try again")

        auth_json: Dict[str, Any] = get_auth_token(
            url = auth_url,
            identifier = username,
            password = password
        )
        auth_token: str = auth_json['accessJwt']

        post_data: Dict[str, Any] = bsky_searched_posts(
            auth_token = auth_token,
            url = posts_url,
            search_phrase = search_phrase,
            required_posts = required_posts,
        )

        with open(output_filepath, 'w') as file:
            json.dump(
                obj = post_data,
                fp = file,
                indent = 4
            )


if __name__ == '__main__':
    obj = BskyData(
        required_posts=500,
        search_phrase="League of Legends" 
    )