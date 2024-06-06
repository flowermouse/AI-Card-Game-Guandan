from sklearn import tree
import matplotlib.pyplot as plt
from joblib import load

clf = load('model/final_tree.joblib')
first_tree = clf.best_estimator_.named_steps['decisiontreeclassifier']

fig, ax = plt.subplots(figsize=(15, 10))
tree.plot_tree(first_tree, ax=ax)
plt.savefig('final_tree.svg')