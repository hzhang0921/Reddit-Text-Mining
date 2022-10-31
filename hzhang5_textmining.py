from itertools import count
from re import T
from venv import create
import praw
import config
import pprint
import nltk
import numpy as np
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd


reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     redirect_uri="http://localhost:8080",
                     user_agent=config.user_agent)
                     

def get_reddit_articles(subreddit):
    """
    Takes a string of a subreddit name and returns a dataframe of
    article titles and article content
    """
    submissions = reddit.subreddit(subreddit).top('day', limit=1000)
    d = {'title': [], 'article_text': []}
    for submission in submissions:
        d['title'].append(submission.title)
        d['article_text'].append(submission.selftext)
    df = pd.DataFrame(data = d)
    return df

def get_reddit_articles_list(subreddit):
    submissions = reddit.subreddit(subreddit).top('day', limit=1000)
    top5 = [(submission.title, submission.selftext) for submission in submissions]
    return top5


def count_words(article_content):
    """
    Take a column of article content and count the
    occurrence of words. return a dictionary with word counts
    """
    list_words = ''.join(article_content).split()
    d = {}
    for word in list_words:
        if word in d:
            d[word] += 1
        else:
            d[word] = 1
    #d2 = dict(sorted(d.items(), key=lambda item: item[1]))
    new = {}
    for (key, value) in d.items():
        if value > 150:
            new[key] = value
    return new


def histogram(word):
    d = {}
    for letters in word:
        if letters not in d:
            d[letters] = 1
        else:
            d[letters] += 1
    return d 


def create_histogram(d):
    f = plt.figure()
    plt.bar(d.keys(), height=d.values())
    plt.xticks(rotation = 45)
    f.set_figwidth(14)
    f.set_figheight(8)
    plt.xlabel("Word")
    plt.ylabel("Word Count")
    plt.title(f"Word Count in Subreddit for '{subreddit}'")
    plt.show()


def average_sentiment(sub):
    top = get_reddit_articles_list(sub)
    dict = {}
    for phrases in top:
        dict[phrases] = SentimentIntensityAnalyzer().polarity_scores(str(phrases))
    list = []
    for keys in dict:
        list.append(dict[keys]['compound'])
    average = 0
    for values in list:
        average += values 
    return average / len(list)


if __name__ == "__main__":
    subreddit = 'mentalhealth'
    print(average_sentiment('wallstreetbets'))
    print(average_sentiment('mentalhealth'))
    print(average_sentiment('happy'))
    print(average_sentiment('leagueoflegends'))
    print(average_sentiment('basketball'))
    df = get_reddit_articles(subreddit)
    d = count_words(df['article_text'])
    print(d)
    create_histogram(d)