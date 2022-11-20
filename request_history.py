import requests
import os
import json
import argparse
import config

# this module was adapted from: 
# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Full-Archive-Search/full-archive-search.py

bearer_token = config.Bearer_Token

search_url = "https://api.twitter.com/2/tweets/search/all"

# not sure this field does anything, the returns have additional fields...
tweet_fields = "text,created_at,public_metrics,author_id,conversation_id,entities,lang,possibly_sensitive,in_reply_to_user_id,attachments,edit_history_tweet_ids,referenced_tweets,reply_settings,source"

# helper function for formating: q_string, start and end are provided as arguments to main 
query_params = lambda q_string, start, end: {'query': q_string, 
                'start_time': start,
                'end_time': end,
                'tweet.fields': tweet_fields,
                'user.fields': 'entities',
                'max_results': 10
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
def main(query_string="Hurricane Ian", start_dtg='2022-09-01T00:00:00Z', end_dtg='2022-11-01T00:00:00Z', query_params=query_params):
    """
    uses the helper function to format the query object with:
    arguments:
        - query_string: the terms to search the tweets for
        - start_dtg: when to begin the search for the terms
        - end_dtg: when to end the search 
        - query_params: the helper function passed in for local scope

    returns:
        - json_reponse: the response object from the Twitter API; 
            - data: first attribute, the list of tweets
            - meta: the details of the request itself
    """
    query_params = query_params(query_string, start_dtg, end_dtg)
    json_response = connect_to_endpoint(search_url, query_params)
    return json_response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="As a module submit query string, start and end date to retrieve Tweets from that range"
    )
    parser.add_argument('--query_string', dest='query_string', action='store', required=True)
    parser.add_argument('--start_date', dest='start_date', action='store', required=True)
    parser.add_argument('--end_date', dest='end_date', action='store', required=True)

    args = parser.parse_args() 

    main(args.query_string, args.start_date, args.end_date)

