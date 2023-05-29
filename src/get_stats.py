import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
aggregated_data_path = os.path.join(data_path, 'aggregated-data.json')
with open(aggregated_data_path, encoding='utf-8') as f:
    agg_d = json.load(f)

id_l = list(agg_d.keys())
# Number of tweets: 4495
key_count_d = {}
for id_t in id_l:
    el = agg_d[id_t]
    key_l = list(el.keys())
    key_l.remove('text')
    len_key_l = len(key_l)
    if len_key_l not in key_count_d.keys():
        key_count_d[len_key_l] = 0
    key_count_d[len_key_l] += 1

# Number of tweets with 1 key: 1728
# Number of tweets with 2 keys: 2767