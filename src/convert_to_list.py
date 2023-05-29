import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
filename = 'aggregated-data-clean-asciified.json'
path = os.path.join(data_path, filename)
with open(path, encoding='utf-8') as f:
    data = json.load(f)

data_l = []
for k, v in data.items():
    new_d = v
    new_d['id'] = k
    data_l.append(new_d)

with open(os.path.join(data_path, filename.replace('.json', '-list.json')), 'w', encoding='utf-8') as f:
    json.dump(data_l, f, indent=4, ensure_ascii=False)
