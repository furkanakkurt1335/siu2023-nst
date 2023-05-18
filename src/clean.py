import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
data_files = [i for i in os.listdir(data_path) if i.endswith('.json')]
clean_path = os.path.join(data_path, 'clean')
if not os.path.exists(clean_path):
    os.mkdir(clean_path)

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
            text = text.lower().strip().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
            while '  ' in text:
                text = text.replace('  ', ' ')
            el['text'] = text
            new_data.append(el)
            continue
    with open(os.path.join(clean_path, file), 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)