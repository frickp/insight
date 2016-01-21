import json
import pandas as pd
import re
import os
import string
import time

#this class loads and cleans the tweets in json format
class TweetManager(object):
    def __init__(self):
        self.PUNCTUATION_MAP = {ord(k): None for k in string.punctuation}
        self.data = []
    
    #each tweet is a dictionary object stored as a list element    
    def load_tweets(self, file_path):
        with open(file_path, 'r') as data_file:
            for line in data_file:
                try:
                    tweet = json.loads(line)
                    self.data.append(tweet)
                except:
                    #skip errors
                    continue
        return self.data
    
    #remove non "basic latin" characters
    def clean_tweets(self, text):
        try:
            clean_tweet = re.sub(r'[^\x20-\x7f]+',r'', text)
        except:
            #if error is found, retain text
            clean_tweet = text
        return clean_tweet
        
    def get_hash_tags(self, text):
        tags = set([self.clean_tag(word[1:]) for word in text.split() if word.startswith('#')])        
        return tags
    
    #remove punctuation marks in hashtags    
    def clean_tag(self, tag):
        #clean punctuations and transform to lower case
        tag = tag.translate(self.PUNCTUATION_MAP)
        tag = tag.lower()
        return tag


#define paths
input_file_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tweet_input'))
input_file_path = input_file_folder + "/tweets.txt"

#load tweets data and cast to a pandas dataframe
tweet_proc = TweetManager()
tweets_data = tweet_proc.load_tweets(input_file_path) 
tweets = pd.DataFrame(tweets_data)

counter = 0

for i, row in tweets.iterrows():
    #clean tweets
    raw_tweet = row['text']
    clean_tweet = tweet_proc.clean_tweets(raw_tweet)
    #if characters were deleted, update data frame
    if (raw_tweet != clean_tweet):
        tweets.set_value(i,'text',clean_tweet)
        counter += 1
    if pd.notnull(tweets['text'][i]) and pd.notnull(tweets['created_at'][i]):
        messageLine = tweets['text'][i] + ' (timestamp: ' + tweets['created_at'][i] + ')'
        print(messageLine)

print('%d tweets contained unicode' % counter)
