import os, json, re

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
data_files = [i for i in os.listdir(data_path) if i.endswith('.json')]
clean_path = os.path.join(data_path, 'clean')
if not os.path.exists(clean_path):
    os.mkdir(clean_path)

url_pattern = 'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)' # taken from https://uibakery.io/regex-library/url
twitter_user_pattern = '@[a-zA-Z0-9_]{1,15}'
for file in data_files:
    with open(os.path.join(data_path, file), encoding='utf-8') as f:
        data = json.load(f)
    data_len = len(data)
    new_data = []
    for i, el in enumerate(data):
        if 'text' in el.keys() and el['text'] != '':
            # deasciify text
            text = el['text']
            text = text.replace('ı', 'i').replace('İ', 'I').replace('ö', 'o').replace('Ö', 'O').replace('ü', 'u').replace('Ü', 'U').replace('ş', 's').replace('Ş', 'S').replace('ç', 'c').replace('Ç', 'C').replace('ğ', 'g').replace('Ğ', 'G')
            text = text.replace('â', 'a').replace('Â', 'A').replace('î', 'i').replace('Î', 'I').replace('û', 'u').replace('Û', 'U')
            # text = text.replace('!', '.').replace('?', '.').replace(';', '.').replace(':', '.').replace(',', '.').replace('.', ' ')
            text = text.lower().strip().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
            text = re.sub(url_pattern, '', text) # remove urls
            text = re.sub(twitter_user_pattern, '', text) # remove twitter users
            while '  ' in text:
                text = text.replace('  ', ' ')
            el['text'] = text.strip()
            new_data.append(el)
            continue
    with open(os.path.join(clean_path, file), 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)