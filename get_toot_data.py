import os
import requests
from functools import lru_cache

# API_TOKEN_TWITTER = os.environ['API_TOKEN_TWITTER']


def create_url(toot_server, toot_id):
    url="https://{}/api/v1/statuses/{}".format(toot_server, toot_id)
    return url


# def bearer_oauth(r):
#     """
#     Method required by bearer token authentication.
#     """

#     r.headers["Authorization"] = f"Bearer {API_TOKEN_TWITTER}"
#     r.headers["User-Agent"] = "v2tootLookupPython"
#     return r


def connect_to_endpoint(url):
    response = requests.request("GET", url)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

@lru_cache(maxsize=8000)
def get_toot_data(toot_server, toot_id):
    url = create_url(toot_server, toot_id)
    json_response = connect_to_endpoint(url)
    print(json_response)
    return(json_response)

@lru_cache(maxsize=8000)
def get_toot_embed(toot_link):

    r = '<iframe src="{}/embed" width="400" height="400" allowfullscreen="allowfullscreen" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-forms"></iframe>'.format(toot_link)
    return(r)