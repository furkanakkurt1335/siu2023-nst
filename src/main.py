import tweepy, os, json
import pandas as pd

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
data_files = os.listdir(data_path)

cred_path = os.path.join(THIS_DIR, 'creds.json')
with open(cred_path) as f:
    creds = json.load(f)

consumer_key, consumer_secret, access_token, access_token_secret = creds['consumer_key'], creds['consumer_secret'], creds['access_token'], creds['access_token_secret']

auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

tweet_d = {}
for file in data_files:
    with open(os.path.join(data_path, file), encoding='utf-8') as f:
        data = json.load(f)
    for i, el in enumerate(data):
        id_t = el['TweetID']
        print(id_t)
        try:
            if id_t in tweet_d.keys():
                text = tweet_d[id_t]
                data[i]['text'] = text
            else:
                tweet = api.get_status(id_t)
                text = tweet.text
                tweet_d[id_t] = text
                data[i]['text'] = text
            print(text)
            print()
        except:
            pass
    with open(os.path.join(data_path, file), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)