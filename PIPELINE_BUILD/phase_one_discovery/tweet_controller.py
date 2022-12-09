import pandas as pd
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
#        self.config = config
        bearer = config.Bearer_Token
        client = tweepy.Client(bearer_token=bearer, wait_on_rate_limit=True)
        self.training_tweet_index = self.raw_training[0]['tweet_id']
        augmented_tweets_training = self.augment_training_text()

    def augment_training_text(self):
        # download the necessary additional fields for the Tweets using the tweet_augmentation functions
        # tweet_augmentation functions are prefaced with ta.<func name>
        try:
            df = self.collect_tweet_dfs(self.training_tweet_index, 0)
        except Exception as e:        
            print("Error in augmenting the training text")
            print(e)

        df = df.drop_duplicates()
        return df 

    def vectorize_text(self):
        pass

    def train_yes_no_model(self):
        pass

    def train_category_model(self):
        pass

    def retrieve_text(index_list):
        list_of_tweets = []
        try:
            tweets = self.client.get_tweets(ids = index_list, tweet_fields = ["author_id", "created_at"])
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

    def collect_tweet_dfs(index_list, start_twt):
        end_twt = start_twt + 100

        tweet_dfs = []

        working = True

        while working: 
            try:
                batch = index_list[start_twt: end_twt]
                df =  self.retrieve_text(batch)
                tweet_dfs.append(df)
                start_twt += 100
                end_twt += 100

            except Exception as e:
                working = False
                print("Error collecting tweets: ", end_twt)
                print(e)
                     
        
        total_dfs = pd.concat(tweet_dfs)
        return total_dfs


