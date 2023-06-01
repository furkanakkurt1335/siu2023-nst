import os, json, argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help='Data directory', required=True)
args = parser.parse_args()

data_path = args.dir
data_files = [i for i in os.listdir(data_path) if i.endswith('.csv')]
sep = [',' if 'sample' in i else ';' for i in data_files]

for i, file in enumerate(data_files):
    base_name = file.replace('.csv', '')
    df = pd.read_csv(os.path.join(data_path, file), sep=sep[i])
    key_l = list(df.keys())
    new_l = []
    for i in range(len(df)):
        new_d = {}
        for key in key_l:
            new_d[key] = str(df[key][i])
        new_l.append(new_d)
    with open(os.path.join(data_path, f'{base_name}.json'), 'w') as f:
        json.dump(new_l, f, indent=4, ensure_ascii=False)
