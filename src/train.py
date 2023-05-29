import os, argparse, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument('--feature', type=str, default='existence', choices=['existence', 'strength', 'category'], help='Feature to train on', required=True)
args = parser.parse_args()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '..', 'data')
filename = 'agg-data-clean-asciified.json'
path = os.path.join(data_path, filename)
with open(path, encoding='utf-8') as f:
    data = json.load(f)

feature = args.feature
out_d = {'feature': feature}

corpus = [el['text'] for el in data if feature in el.keys()]

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3), max_features=1000, lowercase=True)
# existence       0.8014  0.7644
# category        0.7368  0.7066
# strength        0.7607  0.7135

X = vectorizer.fit_transform(corpus)

y = [el[feature] for el in data if feature in el.keys()]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

clf = LogisticRegression(random_state=0).fit(X_train, y_train)
out_d['train_score'] = '{:.4f}'.format(clf.score(X_train, y_train))
out_d['test_score'] = '{:.4f}'.format(clf.score(X_test, y_test))
# print(clf.predict_proba(X_test[:10])) # regression

print('{feature}\t{train_score}\t{test_score}'.format(**out_d))
