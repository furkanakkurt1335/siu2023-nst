import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
filename = 'aggregated-data-clean-asciified-list.json'
path = os.path.join(data_path, filename)
with open(path, encoding='utf-8') as f:
    data = json.load(f)

data_l = []
for el in data:
    new_el = {}
    new_el['id'] = el['id']
    new_el['text'] = el['text']
    if 'HateSpeechExistence' in el.keys():
        new_el['existence'] = el['HateSpeechExistence']
    if 'HateSpeechStrength' in el.keys():
        new_el['strength'] = el['HateSpeechStrength']
    if 'HateSpeechCategory' in el.keys():
        new_el['category'] = el['HateSpeechCategory']
    data_l.append(new_el)

with open(path.replace('.json', '-change.json'), 'w', encoding='utf-8') as f:
    json.dump(data_l, f, indent=4, ensure_ascii=False)
