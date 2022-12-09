import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import time
import config
import tweepy
from tqdm import tqdm

class HurricaneDataHandler():

    """
    HurricaneController manages the data formating, injest and output of the hurricane related tweets:
    - Initialize a HurricaneController
    - Pass the tweet_ids for the collection of tweets to be analyzed to XXXXX

    Requires a config.py file as per the example with Twitter Developer Academic Research permissions.

    """

    def __init__(self, config=config):
        self.raw_training = pd.read_csv('https://raw.githubusercontent.com/Cameron-Grams/Team-HIT-workspace/main/hurricane/website_all_labeled_2016_17_hurricanes.csv'),
        self.ids_and_labels = self.raw_training[0][['tweet_id', 'class_label', 'hurricane']]
        self.client = tweepy.Client( 
                bearer_token = config.Bearer_Token,
                consumer_key = config.API_Key,
                consumer_secret = config.API_Secret,
                wait_on_rate_limit=True
         )
        self.training_tweet_index = self.raw_training[0]['tweet_id']
        self.labeled_with_features = self.augment_training_text()

    def normalize_dates(self, df):
        scaler = MinMaxScaler(feature_range=(0, 100))
        all_hurricanes = []
        hurricanes = df['hurricane'].unique()
        for hurricane in hurricanes:
            print(hurricane)
            df_ = df[ df['hurricane'] == hurricane]
            df_['date'] =  pd.to_datetime(df_['created_at'])
            df_['norm_date'] = scaler.fit_transform(df_['date'].values.reshape(-1,1))
            all_hurricanes.append(df_)
        return pd.concat(all_hurricanes, ignore_index=True)

    def augment_training_text(self):
        # download the necessary additional fields for the Tweets using the tweet_augmentation functions
        # tweet_augmentation functions are prefaced with ta.<func name>
        target = list(self.training_tweet_index)
        try:
            df_ = self.collect_tweet_dfs(target, 0)
        except Exception as e:        
            print("Error in augmenting the training text")
            print(e)
        df = df_.merge(self.ids_and_labels, on='tweet_id', how='inner')
        print("sending df with: ", df.shape)
        df = self.normalize_dates(df)
        print(f"Completed augmentation at {datetime.now()}. Consider rate limiting on API.")
        return df

    def retrieve_tweets(self, index_list):
        list_of_tweets = []
        tweet_fields = ["author_id", 
                "created_at", 
                "conversation_id", 
                "context_annotations",
                "edit_history_tweet_ids",
                "attachments",
                "entities",
                "in_reply_to_user_id",
                 "possibly_sensitive",
                 "public_metrics",
                 "lang",
                 "referenced_tweets",
                 "reply_settings",
                 "source"
                 ]
        try:
            tweets = self.client.get_tweets(ids = index_list, tweet_fields = tweet_fields)
            for tweet in tweets.data:
                current_tweet = {
                    'tweet_id': tweet.id,
                    'text': tweet.text,
                    'author_id': tweet.author_id,
                    'created_at': tweet.created_at or "no_value",
                    'conversation_id': tweet.conversation_id or "no_value",
                    'entities': tweet.entities or "no_value",
                    'context_annotations': tweet.context_annotations or "no_value",
                    "edit_history_tweet_ids": tweet.edit_history_tweet_ids or "no_value",
                    "in_reply_to_user_id": tweet.in_reply_to_user_id or "no_value",
                    "attachments": tweet.attachments or "no_value",
                    "lang": tweet.lang or "no_value", 
                    "possibly_sensitive": tweet.possibly_sensitive or "no_value",
                    "public_metrics": tweet.public_metrics or "no_value",
                    "referenced_tweets": tweet.referenced_tweets or "no_value",
                    "reply_settings": tweet.reply_settings or "no_value",
                    "source": tweet.source or "no_value" 
                }
                current_df = pd.DataFrame([current_tweet])
                list_of_tweets.append(current_df)
            df = pd.concat(list_of_tweets)
            return df

        except Error as e:
            print("Error:", e)
            return False

    def collect_tweet_dfs(self, index_list, start_twt):
        end_twt = start_twt + 100
        tweet_dfs = []
        working = True
        while working: 
            try:
                batch = index_list[start_twt: end_twt]
                df =  self.retrieve_tweets(batch)
                tweet_dfs.append(df)
                start_twt += 100
                end_twt += 100
            except Exception as e:
                working = False
                print(end_twt)
                print(e)
        total_dfs = pd.concat(tweet_dfs)
        return total_dfs


