from flask import Flask, render_template, request

"""Secrets files with API key info"""

import secrets_t
import secrets_r

import sys

import os
import math
import json
from datetime import datetime

from dateutil.parser import parse

import tweepy
import requests
from requests_oauthlib import OAuth1
from chatterbot_functions import *
from cache_and_load_tree import *

TWITTER_JSON = './cache/twitter_tweets.json'
REDDIT_JSON = './cache/reddit_posts.json'
TREE_JSON = './cache/kdTree.json'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", obj_list=None)

@app.template_filter('ctime')
def timectime(s):
    return datetime.fromtimestamp(s)

@app.route("/display_posts", methods=["POST"])
def display_posts():
    category = request.form.get('category')
    x = request.form['topx']
    if type(x) == type(""):
        x = int(x)
    if category == "latest":
        obj_list_l = kd_tree.findTopKMaxD(0, x)
        return render_template("index.html", obj_list=obj_list_l)
    elif category == "most_liked":
        obj_list_ml = kd_tree.findTopKMaxD(1, x)
        return render_template("index.html", obj_list=obj_list_ml)
    elif category == "most_talked_about":
        obj_list_mta = kd_tree.findTopKMaxD(2, x)
        return render_template("index.html", obj_list=obj_list_mta)
    elif category == "hottest":
        obj_list_h = kd_tree.findTopKMaxD(3, x)
        return render_template("index.html", obj_list=obj_list_h)
    else:
        return render_template("index.html", obj_list=None)

if __name__ == "__main__":
    """Twitter authentication parameters!"""

    client_key = secrets_t.TWITTER_API_KEY
    client_secret = secrets_t.TWITTER_API_KEY_SECRET
    access_token = secrets_t.TWITTER_ACCESS_TOKEN
    access_token_secret = secrets_t.TWITTER_ACCESS_TOKEN_SECRET

    auth_t = tweepy.OAuthHandler(client_key, client_secret)
    auth_t.set_access_token(access_token, access_token_secret)
    # Create an API object
    api = tweepy.API(auth_t, wait_on_rate_limit=True)
    # response_twitter = api.search(q="fifaworldcup", lang="en", count=100)

    # print(len(response_twitter))

    """Reddit API"""

    client_id = secrets_r.personal_use_script
    secret_token = secrets_r.secret_token
    reddit_pwd = secrets_r.password
    reddit_user_agent = 'chatterbot507/0.0.1'
    reddit_username = 'ClubIntelligent5370'

    auth_r = requests.auth.HTTPBasicAuth(client_id, secret_token)

    data = {'grant_type': 'password',
            'username': reddit_username,
            'password': reddit_pwd}

    headers = {'User-Agent': reddit_user_agent}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth_r, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    Tweet_list = load_tweets(auth_t, TWITTER_JSON)
    Post_list = load_posts(headers, REDDIT_JSON)

    Nodes = [TreeNode(x) for x in Tweet_list + Post_list]

    if os.path.exists(TREE_JSON) and os.path.getsize(TREE_JSON) != 0:
        kd_tree = load_tree(TREE_JSON)
    else:
        print("Provide valid json tree path! / No cached tree found!")
        kd_tree = kdTree()
    
    for node in Nodes:
        kd_tree.insertNode(node)
    
    store_tree(kd_tree, TREE_JSON)
    app.run(debug=True)