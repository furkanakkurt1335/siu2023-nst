import os, json, re, argparse, string

# parser = argparse.ArgumentParser()
# parser.add_argument('-a', '--asciify', type=str, default='True', help='Whether to asciify the text or not')
# args = parser.parse_args()

# asciify = args.asciify
# if asciify == 'True':
#     asciify = True
# elif asciify == 'False':
#     asciify = False
# print(f'asciify: {asciify}')

url_pattern = 'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)' # taken from https://uibakery.io/regex-library/url
twitter_user_pattern = '@?@[a-zA-Z0-9_]{1,15}'
number_pattern = '[0-9]+'

def clean_text(text):
    text = re.sub(url_pattern, '', text) # remove urls
    text = re.sub(twitter_user_pattern, '', text) # remove twitter users
    text = re.sub(number_pattern, '', text) # remove numbers

    # if asciify:
    #     text = text.replace('ı', 'i').replace('İ', 'I').replace('I', 'i').replace('ö', 'o').replace('Ö', 'O').replace('ü', 'u').replace('Ü', 'U').replace('ş', 's').replace('Ş', 'S').replace('ç', 'c').replace('Ç', 'C').replace('ğ', 'g').replace('Ğ', 'G').replace('â', 'a').replace('Â', 'A').replace('î', 'i').replace('Î', 'I').replace('û', 'u').replace('Û', 'U')

    for punc in string.punctuation:
        text = text.replace(punc, ' ')
    # text = text.lower()
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
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
            new_el['id'] = k
            new_el['text'] = text
            new_el['type'] = el['type']
            if 'existence' in el.keys():
                new_el['existence'] = el['existence']
            if 'strength' in el.keys():
                new_el['strength'] = el['strength']
            if 'category' in el.keys():
                new_el['category'] = el['category']
            data_l.append(new_el)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data_l, f, indent=4, ensure_ascii=False)
    print(f'Wrote {len(data_l)} tweets to {output_path}')

test_files = []
for root, dirs, files in os.walk(data_path):
    for file in files:
        if 'withoutlabels' in file and file.endswith('.json'):
            test_files.append(os.path.join(root, file))

test_data_d = {}
for file in test_files:
    with open(file, encoding='utf-8') as f:
        data = json.load(f)
    if 'isr-pal' in file:
        data_type = 'isr-pal'
    elif 'refugee' in file:
        data_type = 'refugee'
    elif 'tr-gr' in file:
        data_type = 'tr-gr'
    subtask = re.search('Subtask_(\d)', file).group(1)
    for el in data:
        tweet_id = el['TweetID']
        row_id = el['rowID']
        if tweet_id not in test_data_d.keys():
            test_data_d[tweet_id] = {}
        test_data_d[tweet_id]['text'] = clean_text(el['Text'])
        if 'type' not in test_data_d[tweet_id].keys():
            test_data_d[tweet_id]['type'] = data_type
        if 'row_id' not in test_data_d[tweet_id].keys():
            test_data_d[tweet_id]['row_id'] = row_id
        if 'subtask' not in test_data_d[tweet_id].keys():
            test_data_d[tweet_id]['subtask'] = []
        test_data_d[tweet_id]['subtask'].append(subtask)

test_data_l = []
for k, el in test_data_d.items():
    new_el = {}
    if 'row_id' in el.keys():
        new_el['id'] = k
        new_el['row_id'] = el['row_id']
        new_el['type'] = el['type']
        new_el['text'] = el['text']
        new_el['subtask'] = el['subtask']
        test_data_l.append(new_el)

with open(os.path.join(data_path, 'test-data.json'), 'w', encoding='utf-8') as f:
    json.dump(test_data_l, f, indent=4, ensure_ascii=False)
    print(f'Wrote {len(test_data_l)} tweets to {os.path.join(data_path, "test-data.json")}')