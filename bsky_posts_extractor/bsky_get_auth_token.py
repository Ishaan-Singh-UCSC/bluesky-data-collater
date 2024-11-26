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
