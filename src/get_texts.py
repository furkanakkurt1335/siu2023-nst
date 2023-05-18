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
    print('Processing', file)
    with open(os.path.join(data_path, file), encoding='utf-8') as f:
        data = json.load(f)
    data_len = len(data)
    for i, el in enumerate(data):
        if 'text' in el.keys() and el['text'] != '':
            tweet_d[el['TweetID']] = el['text']
            continue
        id_t = el['TweetID']
        try:
            if id_t in tweet_d.keys():
                text = tweet_d[id_t]
                data[i]['text'] = text
            else:
                status = api.get_status(id_t, tweet_mode='extended')
                text = status.full_text
                tweet_d[id_t] = text
                data[i]['text'] = text
        except:
            data[i]['text'] = ''
        if i % 100 == 0:
            print('Remaining', data_len - i)
            with open(os.path.join(data_path, file), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print('Saved', file)
    with open(os.path.join(data_path, file), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print('Saved', file)
    print('Done', file)