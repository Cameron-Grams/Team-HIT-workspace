import requests
import os
import json
import argparse
import config

# this module was adapted from: 
# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Full-Archive-Search/full-archive-search.py

bearer_token = config.Bearer_Token

# helper function to format the end point with the new tweet id
search_url = lambda x: f"https://api.twitter.com/2/tweets/{x}?"

# not sure this field does anything, the returns have additional fields...
tweet_fields = "text,created_at,public_metrics,author_id,conversation_id,entities,lang,possibly_sensitive,in_reply_to_user_id,attachments,edit_history_tweet_ids,referenced_tweets,reply_settings,source"

# helper function for formating: tweet_fields as arguments to main 
query_params = { 
                'tweet.fields': tweet_fields,
                'user.fields': 'entities',
                }

#-------------------------------------------------
# as provided
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r

# as provided
def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
#-------------------------------------------------

# controls the request
def main(tweet_id):
    """
    uses the helper function to format the query object with:
    arguments:
        - tweet_id: the specific tweet to search for

    returns:
        - json_reponse: the response object from the Twitter API; 
            - data: first attribute, the list of tweets
            - meta: the details of the request itself
    """
    search_url = search_url(tweet_id)
    query_params = query_params
    json_response = connect_to_endpoint(search_url, query_params)
    return json_response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="As a module to return historical tweets given tweet id")
    parser.add_argument('--tweet_id', dest='tweet_id', action='store', required=True)

    args = parser.parse_args() 

    main(args.tweet_id)

