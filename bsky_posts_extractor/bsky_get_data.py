from bsky_get_searched_posts import bsky_searched_posts
from bsky_get_auth_token import get_auth_token
from bsky_delete_session import delete_session
from typing import Dict, Any
import os, json


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


# if __name__ == '__main__':
#     obj = BskyData(
#         required_posts=500,
#         search_phrase="League of Legends" 
#     )