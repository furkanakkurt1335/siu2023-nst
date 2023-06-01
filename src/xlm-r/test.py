import os, argparse, json
from transformers import pipeline
from sklearn.metrics import accuracy_score

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--feature', type=str, default='existence', choices=['existence', 'strength', 'category'], help='Feature to train on')
parser.add_argument('-t', '--type', type=str, default='all', choices=['all', 'isr-pal', 'refugee', 'tr-gr'], help='Data type to train on')
parser.add_argument('-s', '--subtask', type=str, help='Subtask to test', choices=['1', '2', '3', '4'])
args = parser.parse_args()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '../../data')
filename = 'data.json'
path = os.path.join(data_path, filename)
with open(path, encoding='utf-8') as f:
    data = json.load(f)

if args.subtask is None:
    test = False
    print('No subtask specified')
    feature = args.feature
else:
    test = True
    print(f'Testing on subtask {args.subtask}')
    test_file = os.path.join(data_path, 'test-data.json')
    with open(test_file, encoding='utf-8') as f:
        test_data = json.load(f)
    test_data_l = [el for el in test_data if args.subtask in el['subtask']]
    print('Test data loaded')
    subtask = args.subtask
    if subtask == '1':
        feature = 'category'
    elif subtask == '2':
        feature = 'existence'
    elif subtask == '3' or subtask == '4':
        feature = 'strength'

print('Testing on feature {}'.format(feature))
out_d = {'feature': feature}

if args.type != 'all':
    print('Using data of type {}'.format(args.type))
    corpus = [el['text'] for el in data if el['type'] == args.type and feature in el.keys()]
    y = [el[feature] for el in data if el['type'] == args.type and feature in el.keys()]
    if test:
        test_corpus = [el['text'] for el in test_data_l if el['type'] == args.type]
else:
    print('Using all data')
    corpus = [el['text'] for el in data if feature in el.keys()]
    y = [el[feature] for el in data if feature in el.keys()]
    print('Train corpus:', corpus[:5])
    print('Train labels:', y[:5])
    if test:
        test_corpus = [el['text'] for el in test_data_l]
        print('Test corpus:', test_corpus[:5])

print('Train data length: {}'.format(len(corpus)))
print('Train labels length: {}'.format(len(y)))
if test:
    print('Test data length: {}'.format(len(test_corpus)))

classifier = pipeline("sentiment-analysis", "cardiffnlp/twitter-xlm-roberta-base-sentiment")
print('Classifier is loaded')

pred_l = []
for el in corpus:
    pred = classifier(el)
    label = pred[0]['label']
    if label == 'negative':
        pred_l.append('1')
    else:
        pred_l.append('0')

acc = accuracy_score(y, pred_l)
print('Accuracy: {}'.format(acc))