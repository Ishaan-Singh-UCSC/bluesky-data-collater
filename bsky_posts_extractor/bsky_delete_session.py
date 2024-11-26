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