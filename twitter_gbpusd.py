# Import Libraries
from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt

# import pycountry
# import re
# import string
# from wordcloud import WordCloud, STOPWORDS
# from PIL import Image
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from langdetect import detect
# from nltk.stem import SnowballStemmer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from sklearn.feature_extraction.text import CountVectorizer


plt.style.use('fivethirtyeight')
# store login data
consumerkey="J3FRxZka044MfPJomBHi3C5Te"
consumersecret="SEoKY5ALUNN0Rroa1fmO3762y1rg3O7OaSH0cVYrPKQXvrDJio"
import requests
# Authentication
BEARER_TOKEN= "AAAAAAAAAAAAAAAAAAAAAKXycgEAAAAA07aphRiO8C%2BkXn86C3KGk46W1ss%3D6RkAEJYPwM6MSAqUT2MrmM0jqQJO5RtwAwSumJP45slgpTAllR"
requests.get(
    'https://api.twitter.com/1.1/search/tweets.json?q=tesla',
    headers={
        'authorization': 'Bearer '+BEARER_TOKEN
})

from datetime import datetime, timedelta
import requests
import pandas as pd

# read bearer token for authentication
# with open('bearer_token.txt') as fp:
#     BEARER_TOKEN = fp.read()

# setup the API request
endpoint = 'https://api.twitter.com/2/tweets/search/recent'
headers = {'authorization': f'Bearer {BEARER_TOKEN}'}
params = {
    'query': '(tesla OR tsla OR elon musk) (lang:en)',
    'max_results': '100',
    'tweet.fields': 'created_at,lang'
}

dtformat = '%Y-%m-%dT%H:%M:%SZ'  # the date format string required by twitter


# we use this function to subtract 60 mins from our datetime string
def time_travel(now, mins):
    now = datetime.strptime(now, dtformat)
    back_in_time = now - timedelta(minutes=mins)
    return back_in_time.strftime(dtformat)


now = datetime.now()  # get the current datetime, this is our starting point
last_week = now - timedelta(days=7)  # datetime one week ago = the finish line
now = now.strftime(dtformat)  # convert now datetime to format for API

df = pd.DataFrame()  # initialize dataframe to store tweets

df = pd.DataFrame()  # initialize dataframe to store tweets
while True:
    if datetime.strptime(now, dtformat) < last_week:
        # if we have reached 7 days ago, break the loop
        break
    pre60 = time_travel(now, 60)  # get 60 minutes before 'now'
    # assign from and to datetime parameters for the API
    params['start_time'] = pre60
    params['end_time'] = now
    response = requests.get(endpoint,
                            params=params,
                            headers=headers)  # send the request
    now = pre60  # move the window 60 minutes earlier
    # iteratively append our tweet data to our dataframe
    for tweet in response.json()['data']:
        row = get_data(tweet)  # we defined this function earlier
        df = df.append(row, ignore_index=True)