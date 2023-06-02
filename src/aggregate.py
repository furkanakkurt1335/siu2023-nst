import os, json, re, argparse, string

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
path = os.path.join(data_path, 'raw')
files = [i for i in os.listdir(path) if i.endswith('.json')]
output_path = os.path.join(data_path, 'data.json')
stopword_path = os.path.join(data_path, 'turkish-stopwords.json')
with open(stopword_path, encoding='utf-8') as f:
    stopwords = json.load(f)
stopword_l = []
for word in stopwords:
    word = word.replace('ı', 'i').replace('İ', 'I').replace('I', 'i').replace('ö', 'o').replace('Ö', 'O').replace('ü', 'u').replace('Ü', 'U').replace('ş', 's').replace('Ş', 'S').replace('ç', 'c').replace('Ç', 'C').replace('ğ', 'g').replace('Ğ', 'G').replace('â', 'a').replace('Â', 'A').replace('î', 'i').replace('Î', 'I').replace('û', 'u').replace('Û', 'U')
    word = word.lower()
    stopword_l.append(word)

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--asciify', type=str, default='True', help='Whether to asciify the text or not')
args = parser.parse_args()

asciify = args.asciify
if asciify == 'True':
    asciify = True
elif asciify == 'False':
    asciify = False
print(f'asciify: {asciify}')

url_pattern = 'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)' # taken from https://uibakery.io/regex-library/url
twitter_user_pattern = '@?@[a-zA-Z0-9_]{1,15}'
number_pattern = '[0-9]+'

def clean_text(text):
    text = re.sub(url_pattern, '', text) # remove urls
    text = re.sub(twitter_user_pattern, '', text) # remove twitter users
    text = re.sub(number_pattern, '', text) # remove numbers

    if asciify:
        text = text.replace('ı', 'i').replace('İ', 'I').replace('I', 'i').replace('ö', 'o').replace('Ö', 'O').replace('ü', 'u').replace('Ü', 'U').replace('ş', 's').replace('Ş', 'S').replace('ç', 'c').replace('Ç', 'C').replace('ğ', 'g').replace('Ğ', 'G').replace('â', 'a').replace('Â', 'A').replace('î', 'i').replace('Î', 'I').replace('û', 'u').replace('Û', 'U')
        text = text.lower()

    for punc in string.punctuation:
        text = text.replace(punc, ' ')
    punc_l = ['…', '“', '”']
    for punc in punc_l:
        text = text.replace(punc, '')
    for stopword in stopword_l:
        pattern = f' {stopword} '
        text = re.sub(pattern, ' ', text)
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    while ' ' in text:
        text = text.replace(' ', '')
    text = text.strip()
    return text

data_l = []
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
        type_t = data_type
        new_el = {'id': tweet_id, 'type': type_t}
        if 'HateSpeechExistence' in el.keys():
            new_el['existence'] = el['HateSpeechExistence']
        if 'HateSpeechStrength' in el.keys():
            new_el['strength'] = el['HateSpeechStrength']
        if 'HateSpeechCategory' in el.keys():
            new_el['category'] = el['HateSpeechCategory']
        if 'text' in el.keys():
            text = clean_text(el['text'])
        if text:
            new_el['text'] = text
            data_l.append(new_el)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data_l, f, indent=4, ensure_ascii=False)
    print(f'Wrote {len(data_l)} tweets to {output_path}')

test_files = []
for root, dirs, files in os.walk(data_path):
    for file in files:
        if 'withoutlabels' in file and file.endswith('.json'):
            test_files.append(os.path.join(root, file))

test_data_l = []
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
        text = clean_text(el['Text'])
        type_t = data_type
        new_el = {'id': tweet_id, 'row_id': row_id, 'text': text, 'type': type_t, 'subtask': subtask}
        test_data_l.append(new_el)

with open(os.path.join(data_path, 'test-data.json'), 'w', encoding='utf-8') as f:
    json.dump(test_data_l, f, indent=4, ensure_ascii=False)
    print(f'Wrote {len(test_data_l)} tweets to {os.path.join(data_path, "test-data.json")}')