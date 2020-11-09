# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 20:19:01 2020

@author: Evelyn
"""

#!pip install tweepy
import tweepy

#%% token
API_Key = "44RW9iNKirbKGMS16MriffCIs"
API_Secret_Key = "TcczPSw4p0ahN2V74V5LC3lB8gt5MuBvVYmevfYZqgqEq2TvlL"
Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAIQPIgEAAAAA0PWsCtCETHVv6blJPcUd%2Bc1bzuU%3D38TqONvW3cAY5iw8rWInuzG6x0EDxrOV5ZElZkoHnaJ2ZUX3OY"
Access_token = "713695819-8MiG97wqfNpmHHWunFcFYKjb31yviUsIJ7lzTEh0"
Access_toekn_secret = "8LnBDuJZb6ffjCo7SNNE4PoRDxv9YquNzbPAtQSnV6ndU"

#%% connect to twitter
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy as tw
import json
import pandas as pd
import csv
import re
from textblob import TextBlob
import string
import os
import time
import datetime

## connect to API
auth = OAuthHandler(API_Key,API_Secret_Key)
auth.set_access_token(Access_token, Access_toekn_secret)
api = tw.API(auth)

#connection test
#public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

#%% define functions

def conv_date2str(date):
  if type(date) is str:
    return date
  elif (type(date) is pd.Timestamp) or (type(date) is datetime.datetime):
    return date.strftime("%Y-%m-%d")
  else:
    print('Invalid date type! Please change to "YYYY-MM-DD"')
    return None
    
def tweetscraper(ticker, start_date, end_date, numTweets=1000):
  ## check date type
  if conv_date2str(start_date) is not None:
    start_date = conv_date2str(start_date)
  else:
    return None

  if conv_date2str(end_date) is not None:
    end_date = conv_date2str(end_date)
  else:
    return None
    ## create a database
  db_tweets = pd.DataFrame(columns = ['username', 'location', 'following','followers','totaltweets','usercreatedts','tweetcreatedts','retweetcount','text']) 
  program_start = time.time() ## time each call
  tweets =  tw.Cursor(api.search, q=str(ticker), lang="en", since=start_date, until=end_date, tweet_mode='extended').items(numTweets) # get numTweets of tweets for each run
  tweet_list = [tweet for tweet in tweets]

  ## get values from each tweet
  for tweet in tweet_list:
    username = tweet.user.screen_name
    location = tweet.user.location
    following = tweet.user.friends_count
    followers = tweet.user.followers_count
    totaltweets = tweet.user.statuses_count
    usercreatedts = tweet.user.created_at
    tweetcreatedts = tweet.created_at
    retweetcount = tweet.retweet_count
    text = tweet.full_text

    ith_tweet = [username, location, following, followers, totaltweets, usercreatedts, tweetcreatedts, retweetcount, text]
    db_tweets.loc[len(db_tweets)] = ith_tweet # append to database

  program_end = time.time()
  print('Scraping has completed!')
  print('Total time taken to scrap is {} minutes.'.format(round(program_end-program_start)/60,2)) 
  return db_tweets

#%% get tweets
ticker = "@JoeBiden"
start_date = "2020-11-02"
end_date = "2020-11-03"#datetime.datetime.today().strftime("%Y-%m-%d")

stock_tweets = tweetscraper(ticker, start_date, end_date)
Trump = tweetscraper("Trump", start_date, end_date) 
Biden = tweetscraper("Joe Biden", start_date, end_date)

tweet_biden = Biden['text'].copy()
tweet_trump = Trump['text'].copy()
#%% data processing
#from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
#from nltk.tokenize import word_tokenize
#import re
#
#tweet = stock_tweets['text'].copy()
#for i in range(len(tweet)):
#    if len(re.findall("\$[A-Z]{1,4}",tweet[i]))>4:
#        tweet[i] = ""
##    elif len(re.findall("[T,t]rump",tweet[i]))>0:
##        tweet[i] = ""
#
## tokenize
#tweet_token = tweet.apply(word_tokenize)
#
## remove puctuations and figures
#all_words = r"[A-Za-z]\w+"
#tweet_words = tweet_token.apply(lambda x: re.findall(all_words,str(x)))
#
#
## Create a list of stopwords and remove them from the tokens list (only_words)
#tweet_nosw = [[i for i in tweet_words[j] if i not in ENGLISH_STOP_WORDS] for j in range(len(tweet_words))]
#
## change all to uppercase
#tweet_up = [[str.upper(i) for i in tweet_nosw[j]] for j in range(len(tweet_nosw))]

#%% define Sentiment analysis for words
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wnet

def sentiment_analyzer(words):
    words = words.to_frame()
    #print(words)
    analyzer = SentimentIntensityAnalyzer()
    word_pos = []
    word_neu = []
    word_neg = []
    word_comp = []

    for i in range(len(words)):
        word_pos_score = 0
        word_neg_score = 0
        word_neu_score = 0
        word_comp_score = 0
        for word in words.iloc[i]:
            vs = analyzer.polarity_scores(word)
            word_pos_score += vs['pos']
            word_neg_score += vs['neg']
            word_neu_score += vs['neu']
            word_comp_score += vs['compound']
        word_pos.append(word_pos_score)
        word_neu.append(word_neu_score)
        word_neg.append(word_neg_score)
        word_comp.append(word_comp_score)
    #print(word_pos, word_neu)
    result = words.assign(**{'Positive Score by Word': word_pos,'Neutrual Score by Word':word_neu,'Negative Score by Word': word_neg, 'Compound Score by Word': word_comp})
    return result

#%% sentiment analysis by words

tweet_biden_token = tweet_biden.apply(word_tokenize)
tweet_trump_token = tweet_trump.apply(word_tokenize)

result_biden_word = sentiment_analyzer(tweet_biden_token)
result_trump_word = sentiment_analyzer(tweet_trump_token)

#%% sentiment analysis for sentences
sent_biden_token = tweet_biden.apply(sent_tokenize)
sent_trump_token = tweet_trump.apply(sent_tokenize)

result_biden_sent = sentiment_analyzer(sent_biden_token)
result_trump_sent = sentiment_analyzer(sent_trump_token)

#%% plot the comparison
import matplotlib.pyplot as plt
plt.hist(result_biden_sent['Compound Score by Word']*Biden['retweetcount'],
         bins=50, alpha=0.5, color="royalblue", histtype="bar")
plt.hist(result_trump_sent['Compound Score by Word']*Trump['retweetcount'],
         bins=50, alpha=0.5, color="red", histtype="bar")
plt.legend(["Biden", "Trump"])
plt.rcParams["font.size"] = "14"