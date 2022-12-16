# chatterbot507
This is my project code for the SI507 Intermediate programming course. 

The API keys for the reddit and twitter APIs are placed in the secrets_r.py and secrets_t.py files respectively (submitted in canvas for use by the SI 507 teaching team, not included in the github to ensure my privacy). The instructions to set up a twitter developer account and generate the relevant API keys are as specified in the lecture slides. As for the reddit API keys, I followed the instructions specified in the below website: 
https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
Once the keys are generated and placed in the respective secret_*.py files, these files are imported by the main program (chatterbot_flask.py). The following authentication parameters are required for each API, Twitter: 1) client_key 2) client_key_secret 3) access_token 4) access_token_secret, Reddit: 1) client_id 2) secret_token 3) reddit username 4) reddit_password 5) reddit_user_agent. 
The chatterbot_functions.py file contains the helper functions for tasks such as accessing the API and caching as well as the class definitions for tweets/posts and trees. The chatterbot_flask.py file contains the main program for deploying a flask server. This file imports the chatterbot_functions.py file. Run the chatterbot_flask.py to run the code for this project. Open the url specified in the terminal on a web browser, select the desired options from the radio buttons and click submit to view the posts/tweets of a particular category.
The following additional python packages are required for the project code to run: 1) Flask 2) tweepy 3) requests 4) requests_oauthlib 5) datetime 6) dateutil.parser.

