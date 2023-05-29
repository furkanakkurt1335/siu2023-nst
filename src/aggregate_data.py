import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
raw_path = os.path.join(data_path, 'raw')
clean_path = os.path.join(data_path, 'clean')
data_files = [i for i in os.listdir(raw_path) if i.endswith('.json')]

data_d = {}
for data_file in data_files:
    with open(os.path.join(raw_path, data_file), encoding='utf-8') as f:
        data = json.load(f)
    for el in data:
        tweet_id = el['TweetID']
        del el['TweetID']
        if tweet_id not in data_d.keys():
            data_d[tweet_id] = el
        else:
            key_l = list(el.keys())
            for key in key_l:
                if key not in data_d[tweet_id].keys():
                    data_d[tweet_id][key] = el[key]

with open(os.path.join(data_path, 'aggregated-data-raw.json'), 'w', encoding='utf-8') as f:
    json.dump(data_d, f, indent=4, ensure_ascii=False)