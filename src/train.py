import os, argparse, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--feature', type=str, default='existence', choices=['existence', 'strength', 'category'], help='Feature to train on')
parser.add_argument('--data_type', type=str, default='all', choices=['all', 'isr-pal', 'refugee', 'tr-gr'], help='Data type to train on')
args = parser.parse_args()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
filename = 'data.json'
path = os.path.join(data_path, filename)
with open(path, encoding='utf-8') as f:
    data = json.load(f)

feature = args.feature
out_d = {'feature': feature}

if args.data_type != 'all':
    corpus = [el['text'] for el in data if el['type'] == args.data_type and feature in el.keys()]
else:
    corpus = [el['text'] for el in data if feature in el.keys()]

text_len_l = [len(el) for el in corpus]

max_features = 3000
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3), max_features=max_features, lowercase=True)

X = vectorizer.fit_transform(corpus)

vectorizer = TfidfVectorizer(max_features=max_features, lowercase=True)

X_t = vectorizer.fit_transform(corpus)

X = np.concatenate((X.toarray(), X_t.toarray()), axis=1)

if args.data_type != 'all':
    y = [el[feature] for el in data if el['type'] == args.data_type and feature in el.keys()]
else:
    y = [el[feature] for el in data if feature in el.keys()]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# clf = make_pipeline(StandardScaler(with_mean=False), SVC(gamma='auto')).fit(X_train, y_train)
clf = LogisticRegression(random_state=0).fit(X_train, y_train)
out_d['train_score'] = '{:.4f}'.format(clf.score(X_train, y_train))
out_d['test_score'] = '{:.4f}'.format(clf.score(X_test, y_test))
# print(clf.predict_proba(X_test[:10])) # regression

print('{feature}\t{train_score}\t{test_score}'.format(**out_d))
# existence       0.8582  0.7471
# category        0.8550  0.6967
# strength        0.8161  0.7290