import sys

import secrets_t
import secrets_r

import os
import math
import json
from datetime import datetime

from dateutil.parser import parse

import tweepy
import requests
from requests_oauthlib import OAuth1
from chatterbot_functions import *

TREE_JSON = './cache/kdTree.json'

def cache_tree(root):
  if root is None:
    return None
  json_data = {}
  json_data['object_ref'] = root.object_ref.__dict__
  json_data['left'] = cache_tree(root.left)
  json_data['right'] = cache_tree(root.right)  
  return json_data

def store_tree(kd_tree, json_cache_path):
  treeDict = cache_tree(kd_tree.root)
  json_data = dict()
  json_data['data'] = treeDict
  with open(json_cache_path, "w") as cfile:
    json.dump(json_data, cfile)

def construct_tree(treeDict):
  # Base case
  if treeDict is None:
    return None
  objd = treeDict['object_ref']
  if objd['type'] == "Tweet":
    treeNode = TreeNode(Tweet(json_record=objd))
  else:
    treeNode = TreeNode(Post(json_record=objd))  
  treeNode.left = construct_tree(treeDict['left'])
  treeNode.right = construct_tree(treeDict['right'])
  return treeNode

def load_tree(json_cache_path):
  kd_tree = kdTree()
  with open(json_cache_path, 'r') as tfile:
    treeDict = json.load(tfile).get('data')
  kd_tree.root = construct_tree(treeDict)
  return kd_tree

def main():
    if os.path.exists(TREE_JSON) and os.path.getsize(TREE_JSON) != 0:
        kd_tree = load_tree(TREE_JSON)
    else:
        print("Provide valid json tree path!")


if __name__ == "__main__":
    main()