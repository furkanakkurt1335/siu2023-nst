import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
selected = 'raw'
if selected == 'clean':
    path = os.path.join(data_path, 'clean')
elif selected == 'raw':
    path = os.path.join(data_path, 'raw')
elif selected == 'clean-asciified':
    path = os.path.join(data_path, 'clean-asciified')
data_files = [i for i in os.listdir(path) if i.endswith('.json')]

data_d = {}
for data_file in data_files:
    with open(os.path.join(path, data_file), encoding='utf-8') as f:
        data = json.load(f)
    for el in data:
        tweet_id = el['TweetID']
        if tweet_id not in data_d.keys():
            data_d[tweet_id] = {}
        if 'HateSpeechExistence' in el.keys():
            data_d[tweet_id]['existence'] = el['HateSpeechExistence']
        if 'HateSpeechStrength' in el.keys():
            data_d[tweet_id]['strength'] = el['HateSpeechStrength']
        if 'HateSpeechCategory' in el.keys():
            data_d[tweet_id]['category'] = el['HateSpeechCategory']
        if 'text' in el.keys():
            data_d[tweet_id]['text'] = el['text']

data_l = []
for k, v in data_d.items():
    new_d = v
    new_d['id'] = k
    data_l.append(new_d)

with open(os.path.join(data_path, 'agg-data-{}.json'.format(selected)), 'w', encoding='utf-8') as f:
    json.dump(data_l, f, indent=4, ensure_ascii=False)