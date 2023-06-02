import os, argparse, json
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB

feature_l = ['existence', 'strength', 'category']
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--feature', type=str, default='existence', help='Feature to train on')
parser.add_argument('-t', '--type', type=str, default='all', choices=['all', 'isr-pal', 'refugee', 'tr-gr'], help='Data type to train on')
parser.add_argument('-s', '--subtask', type=str, help='Subtask to test', choices=['1', '2', '3', '4'])
args = parser.parse_args()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
filename = 'data.json'
path = os.path.join(data_path, filename)
with open(path, encoding='utf-8') as f:
    data = json.load(f)

if args.subtask is None:
    test = False
    print('No subtask specified')
    feature = args.feature
    possible_features = []
    for f in feature_l:
        if f.startswith(feature):
            possible_features.append(f)
    if len(possible_features) == 0:
        raise ValueError('Feature {} not found'.format(feature))
    elif len(possible_features) > 1:
        raise ValueError('Multiple features found: {}'.format(possible_features))
    else:
        feature = possible_features[0]
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

print('Training on feature {}'.format(feature))
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

max_features = 10000
print('Max features: {}'.format(max_features))
vectorizer1 = TfidfVectorizer(max_features=max_features, ngram_range=(1, 3), analyzer='word')
vectorizer2 = TfidfVectorizer(max_features=max_features, ngram_range=(1, 3), analyzer='char')
vectorizer3 = CountVectorizer(max_features=max_features, ngram_range=(1, 3), analyzer='char')

X_train = vectorizer1.fit_transform(corpus)
X_t = vectorizer2.fit_transform(corpus)
X_train = np.concatenate((X_train.toarray(), X_t.toarray()), axis=1)
X_t = vectorizer3.fit_transform(corpus)
X_train = np.concatenate((X_train, X_t.toarray()), axis=1)

# add length
add_len = False
if add_len:
    length = np.array([len(el) for el in corpus]).reshape(-1, 1)
    X_train = np.concatenate((X_train, length), axis=1)
print('Len added: {}'.format(add_len))

if test:
    X_test = vectorizer1.transform(test_corpus)
    X_test_t = vectorizer2.transform(test_corpus)
    X_test = np.concatenate((X_test.toarray(), X_test_t.toarray()), axis=1)
    X_test_t = vectorizer3.transform(test_corpus)
    X_test = np.concatenate((X_test, X_test_t.toarray()), axis=1)
    if add_len:
        test_length = np.array([len(el) for el in test_corpus]).reshape(-1, 1)
        X_test = np.concatenate((X_test, test_length), axis=1)

if not test:
    X_train, X_test, y_train, y_test = train_test_split(X_train, y, test_size=0.2, random_state=42)
    print('Splitting train data into train and test sets')
else:
    X_train, y_train = X_train, y

scale = False
if scale:
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    # scaler = StandardScaler()
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    if test:
        X_test = scaler.transform(X_test)
print('Scaled: {}'.format(scale))

max_iter = 1000
print('Max iter: {}'.format(max_iter))

clf = LogisticRegression(max_iter=max_iter, random_state=42)

print('Training with {} classifier'.format(clf))

clf.fit(X_train, y_train)

train_score = clf.score(X_train, y_train)
out_d['train_score'] = '{:.4f}'.format(train_score)
if not test:
    test_score = clf.score(X_test, y_test)
    out_d['test_score'] = '{:.4f}'.format(test_score)
    print('{feature}\t{train_score}\t{test_score}'.format(**out_d))
else:
    print('{feature}\t{train_score}'.format(**out_d))
    y_pred = clf.predict(X_test)
    if subtask == '1':
        sample_key = 'HateSpeechCategory'
        if feature != 'category':
            raise ValueError('Feature must be category for subtask 1')
    elif subtask == '2':
        sample_key = 'HateSpeechExistence'
        if feature != 'existence':
            raise ValueError('Feature must be existence for subtask 2')
    elif subtask == '3' or subtask == '4':
        sample_key = 'HateSpeechStrength'
        if feature != 'strength':
            raise ValueError('Feature must be strength for subtask 3 or 4')
    df = pd.DataFrame({'rowID': [i['row_id'] for i in test_data_l], sample_key: y_pred})
    df.to_csv(os.path.join(data_path, f'subtask{args.subtask}_{feature}_submission.csv'), index=False)
