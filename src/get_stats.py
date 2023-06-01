import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
aggregated_data_path = os.path.join(data_path, 'data.json')
with open(aggregated_data_path, encoding='utf-8') as f:
    data_l = json.load(f)

# Number of tweets: 4495
key_count_d = {}
for el in data_l:
    key_l = list(el.keys())
    key_l.remove('text')
    key_l.remove('id')
    key_l.remove('type')
    len_key_l = len(key_l)
    if len_key_l not in key_count_d.keys():
        key_count_d[len_key_l] = 0
    key_count_d[len_key_l] += 1

print(key_count_d)

# Number of tweets with 1 key: 343
# Number of tweets with 2 keys: 4150