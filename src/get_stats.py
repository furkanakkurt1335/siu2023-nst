import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data', 'clean')
data_files = [i for i in os.listdir(data_path) if i.endswith('.json')]

for file in data_files:
    counter_d = {}
    with open(os.path.join(data_path, file), encoding='utf-8') as f:
        data = json.load(f)
    keys = list(data[0].keys())
    keys.remove('TweetID')
    keys.remove('text')
    count_key = keys[0]
    for el in data:
        val = el[count_key]
        if val not in counter_d.keys():
            counter_d[val] = 0
        counter_d[val] += 1
    print(file)
    print(count_key)
    print(counter_d)
    print()
