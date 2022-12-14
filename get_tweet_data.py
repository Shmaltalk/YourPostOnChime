import os
import requests

API_TOKEN_TWITTER = os.environ['API_TOKEN_TWITTER']


def create_url(tweet_id):
    tweet_fields = "tweet.fields=text,context_annotations"
    expansions = "expansions=attachments.media_keys"
    media_fields = "media.fields=url,alt_text"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "ids={}".format(tweet_id)
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}&{}&{}".format(ids, tweet_fields,expansions,media_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {API_TOKEN_TWITTER}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_tweet_data(tweet_id):
    url = create_url(tweet_id)
    json_response = connect_to_endpoint(url)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    return(json_response)


def get_tweet_embed(tweet_link):
    r = requests.get('https://publish.twitter.com/oembed?url={}&hide_thread=true'.format(tweet_link))
    return(r.json()["html"])