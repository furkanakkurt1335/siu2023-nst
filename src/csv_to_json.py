import tweepy, os, json
import pandas as pd

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
data_files = [i for i in os.listdir(data_path) if i.endswith('.csv')]

for file in data_files:
    base_name = file.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_path, file), sep=';')
    key_l = list(df.keys())
    new_l = []
    for i in range(len(df)):
        new_d = {}
        for key in key_l:
            new_d[key] = str(df[key][i])
        new_l.append(new_d)
    with open(os.path.join(data_path, f'{base_name}.json'), 'w') as f:
        json.dump(new_l, f, indent=4, ensure_ascii=False)
