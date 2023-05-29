import os, json, re

url_pattern = 'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)' # taken from https://uibakery.io/regex-library/url
twitter_user_pattern = '@[a-zA-Z0-9_]{1,15}'
number_pattern = '[0-9]+'

def clean_text(text, asciify=True):
    text = re.sub(url_pattern, '', text) # remove urls
    text = re.sub(twitter_user_pattern, '', text) # remove twitter users
    text = re.sub(number_pattern, '', text) # remove numbers

    # asciify text
    if asciify:
        text = text.replace('ı', 'i').replace('İ', 'I').replace('ö', 'o').replace('Ö', 'O').replace('ü', 'u').replace('Ü', 'U').replace('ş', 's').replace('Ş', 'S').replace('ç', 'c').replace('Ç', 'C').replace('ğ', 'g').replace('Ğ', 'G')
        text = text.replace('â', 'a').replace('Â', 'A').replace('î', 'i').replace('Î', 'I').replace('û', 'u').replace('Û', 'U')

    # text = text.replace('!', '.').replace('?', '.').replace(';', '.').replace(':', '.').replace(',', '.').replace('.', ' ')
    text = text.lower()
    text = text.strip().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return text

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
path = os.path.join(data_path, 'raw')
files = [i for i in os.listdir(path) if i.endswith('.json')]
output_path = os.path.join(data_path, 'data.json')

data_d = {}
for file in files:
    filepath = os.path.join(path, file)
    if 'isr-pal' in file:
        data_type = 'isr-pal'
    elif 'refugee' in file:
        data_type = 'refugee'
    elif 'tr-gr' in file:
        data_type = 'tr-gr'
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)
    for el in data:
        tweet_id = el['TweetID']
        if tweet_id not in data_d.keys():
            data_d[tweet_id] = {}
        if 'type' not in data_d[tweet_id].keys():
            data_d[tweet_id]['type'] = data_type
        if 'HateSpeechExistence' in el.keys():
            data_d[tweet_id]['existence'] = el['HateSpeechExistence']
        if 'HateSpeechStrength' in el.keys():
            data_d[tweet_id]['strength'] = el['HateSpeechStrength']
        if 'HateSpeechCategory' in el.keys():
            data_d[tweet_id]['category'] = el['HateSpeechCategory']
        if 'text' in el.keys():
            data_d[tweet_id]['text'] = clean_text(el['text'])

data_l = []
for k, el in data_d.items():
    new_el = {}
    if 'text' in el.keys() and el['text'] != '':
        text = el['text']
        if text:
            new_el['text'] = text
            new_el['type'] = el['type']
            if 'existence' in el.keys():
                new_el['existence'] = el['existence']
            if 'strength' in el.keys():
                new_el['strength'] = el['strength']
            if 'category' in el.keys():
                new_el['category'] = el['category']
            data_l.append(el)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data_l, f, indent=4, ensure_ascii=False)
