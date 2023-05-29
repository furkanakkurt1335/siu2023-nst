import os, argparse, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

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
# existence       0.9287  0.8901
# category        0.8818  0.8922
# strength        0.8287  0.8054

X = vectorizer.fit_transform(corpus)

y = [el[feature] for el in data if feature in el.keys()]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

clf = make_pipeline(StandardScaler(with_mean=False), SVC(gamma='auto')).fit(X, y)
out_d['train_score'] = '{:.4f}'.format(clf.score(X_train, y_train))
out_d['test_score'] = '{:.4f}'.format(clf.score(X_test, y_test))
# print(clf.predict_proba(X_test[:10])) # regression

print('{feature}\t{train_score}\t{test_score}'.format(**out_d))
