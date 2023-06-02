import os, json, argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, help='Data file', required=True)
args = parser.parse_args()

file_path = args.file

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')

base_name = os.path.basename(file_path).replace('.xls', '')
df = pd.read_excel(file_path)
key_l = list(df.keys())

word_l = []
for i in range(len(df)):
    new_d = {}
    for key in key_l:
        new_d[key] = str(df[key][i])
    word_l.append(new_d['KELIME'])

with open(os.path.join(data_path, f'{base_name}.json'), 'w') as f:
    json.dump(word_l, f, indent=4, ensure_ascii=False)
