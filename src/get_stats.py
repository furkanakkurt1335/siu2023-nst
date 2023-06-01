import os, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--feature', type=str, default='existence', choices=['existence', 'strength', 'category'])
parser.add_argument('-s', '--subtask', type=str, default='1', choices=['1', '2', '3', '4'])
args = parser.parse_args()

if args.subtask:
    import pandas as pd
    subtask = args.subtask
    if subtask == '1':
        feature = 'category'
    elif subtask == '2':
        feature = 'existence'
    elif subtask == '3' or subtask == '4':
        feature = 'strength'
else:
    feature = args.feature

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
data_file = os.path.join(data_path, 'data.json')
with open(data_file, encoding='utf-8') as f:
    data_l = json.load(f)

# Number of tweets: 4495
# key_count_d = {}
# for el in data_l:
#     key_l = list(el.keys())
#     key_l.remove('text')
#     key_l.remove('id')
#     key_l.remove('type')
#     len_key_l = len(key_l)
#     if len_key_l not in key_count_d.keys():
#         key_count_d[len_key_l] = 0
#     key_count_d[len_key_l] += 1

# print(key_count_d)

# Number of tweets with 1 key: 343
# Number of tweets with 2 keys: 4150

selected_data = [el for el in data_l if feature in el.keys()]
count_d = {}
for el in data_l:
    if feature in el.keys():
        if el[feature] not in count_d.keys():
            count_d[el[feature]] = 0
        count_d[el[feature]] += 1

print('Feature: {}'.format(feature))
for n in sorted(count_d.keys()):
    print('Number of {}: {}'.format(n, count_d[n]))

if args.subtask:
    print('\nSubmission data')
    submission_files = [i for i in os.listdir(data_path) if 'subtask{}'.format(args.subtask) in i]
    subm_path = os.path.join(data_path, submission_files[0])
    subm_data = pd.read_csv(subm_path, sep=',')
    subm_count_d = {}
    for el in subm_data.iloc[:, 1]:
        if el not in subm_count_d.keys():
            subm_count_d[el] = 0
        subm_count_d[el] += 1  
    for n in sorted(subm_count_d.keys()):
        print('Number of {}: {}'.format(n, subm_count_d[n]))