import os, argparse, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument('--feature', type=str, default='existence', choices=['existence', 'strength', 'category'], help='Feature to train on', required=True)
args = parser.parse_args()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
filename = 'aggregated-data-clean-asciified-list-change.json'
path = os.path.join(data_path, filename)
with open(path, encoding='utf-8') as f:
    data = json.load(f)

feature = args.feature
print('Feature: {}'.format(feature))

corpus = [el['text'] for el in data if feature in el.keys()]
print('Corpus length: {}'.format(len(corpus)))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print('Feature names: {}'.format(vectorizer.get_feature_names_out()))
print('Shape: {}'.format(X.shape))

y = [el[feature] for el in data if feature in el.keys()]
print('Labels length: {}'.format(len(y)))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

clf = LogisticRegression(random_state=0).fit(X_train, y_train)
print('Train score: {}'.format(clf.score(X_train, y_train)))
print('Test score: {}'.format(clf.score(X_test, y_test)))