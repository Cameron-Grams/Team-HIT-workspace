import pandas as pd

def retrieve_text(index_list):
    list_of_tweets = []
    try:
        tweets = client.get_tweets(ids = index_list, tweet_fields = ["author_id", "created_at"])
        for tweet in tweets.data:
            current_tweet = {
                'tweet_id': tweet.id,
                'text': tweet.text,
                'author_id': tweet.author_id,
                'created_at': tweet.created_at
            }
            current_df = pd.DataFrame([current_tweet])
            list_of_tweets.append(current_df)
        df = pd.concat(list_of_tweets)
        return df

    except Error as e:
        print("Error:", e)
        return False

# --------------

def collect_tweet_dfs(index_list, start_twt):
    end_twt = start_twt + 100

    tweet_dfs = []

    working = True

    while working: 
        try:
            batch = index_list[start_twt: end_twt]
            df =  retrieve_text(batch)
            tweet_dfs.append(df)
            start_twt += 100
            end_twt += 100

        except Exception as e:
            working = False
            print(end_twt)
            print(e)
                 
    
    total_dfs = pd.concat(tweet_dfs)
    return total_dfs

#--------------------------------

tweet_fields = ['tweet_id',
            'text',
            'author_id',
            'created_at',
            'conversation_id',
            'entities',
            'context_annotations',
            "edit_history_tweet_ids",
            "in_reply_to_user_id",
            "attachments",
            "lang", 
            "possibly_sensitive",
            "public_metrics",
            "referenced_tweets",
            "reply_settings",
            "source"]
