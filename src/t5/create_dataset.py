from datasets import load_dataset, DatasetDict
import os, json, argparse

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--feature', type=str, required=True)
args = parser.parse_args()

number_d = {'0': 'sıfır', '1': 'bir', '2': 'iki', '3': 'üç', '4': 'dört', '5': 'beş', '6': 'altı', '7': 'yedi', '8': 'sekiz', '9': 'dokuz'}

feature = args.feature
dataset_path = os.path.join(THIS_DIR, 'datasets', feature)
dataset_name = 'nst-{}'.format(feature)
print('Dataset:', dataset_name)
print('Loading dataset...')
dataset = load_dataset('json', data_files='data.json')
print('Dataset is loaded.')

new_data = []
for i, el in enumerate(dataset['train']):
    if el[feature]:
        new_data.append({'text': el['text'], feature: el[feature], 'id': el['id']})
with open('data-{}.json'.format(feature), 'w') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)
dataset = load_dataset('json', data_files='data-{}.json'.format(feature))

train_test_dataset = dataset['train'].train_test_split(test_size=0.1)
valid_test_dataset = train_test_dataset['test'].train_test_split(test_size=0.5)

dataset = DatasetDict({
    'train': train_test_dataset['train'],
    'validation': valid_test_dataset['train'],
    'test': valid_test_dataset['test'],
})

print('Shuffling dataset...')
dataset['train'] = dataset['train'].shuffle(seed=42)
dataset['validation'] = dataset['validation'].shuffle(seed=42)
dataset['test'] = dataset['test'].shuffle(seed=42)
print('Dataset is shuffled.')

# save dataset
dataset.save_to_disk(dataset_path)

print('Dataset size:', len(dataset['train']) + len(dataset['test']))
print('Train size:', len(dataset['train']))
print('Test size:', len(dataset['test']))
print('Dataset:', dataset)
