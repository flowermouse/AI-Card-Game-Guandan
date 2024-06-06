from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import csv
from joblib import dump

from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

model_name = 'final_tree.joblib'
data_name = 'data/data7.csv'

def read_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return data[1:]

def code_data(string):
    n3 = string.count('3')
    n4 = string.count('4')
    n5 = string.count('5')
    n6 = string.count('6')
    n7 = string.count('7')
    n8 = string.count('8')
    n9 = string.count('9')
    n10 = string.count('10')
    nj = string.count('J')
    nq = string.count('Q')
    nk = string.count('K')
    na = string.count('A')
    n2 = string.count('2')
    coded = [n3, n4, n5, n6, n7, n8, n9, n10, nj, nq, nk, na, n2]
    return coded


def train_decision_tree(data):
    X = []
    y = []
    for row in data:
        if int(row[1]) - int(row[2]) <= 25:
            sample = eval(row[4]) + eval(row[5]) + code_data(row[6])
            X.append(sample)
            y.append(int(row[3]))
    # clf = tree.DecisionTreeClassifier()
    # clf = clf.fit(X, y)
     # 创建一个预处理和分类的pipeline
    pipeline = make_pipeline(StandardScaler(), tree.DecisionTreeClassifier())

    # 定义要搜索的参数
    param_grid = {'decisiontreeclassifier__max_depth': [3, 5, 7, 10, 15, 20],
                  'decisiontreeclassifier__min_samples_split': [2, 5, 10, 15, 20, 30],
                  'decisiontreeclassifier__criterion': ['gini', 'entropy']}

    # 使用网格搜索和交叉验证
    clf = GridSearchCV(pipeline, param_grid, cv=5)
    clf = clf.fit(X, y)
    return clf

def train_combat_tree(data):
    X = []
    y = []
    mymap = {'combat':0, 'bomb':1, 'pass':2}
    for row in data:
        if int(row[1]) - int(row[2]) <= 25 and row[8] != 'best':
            sample = eval(row[3]) + eval(row[4]) + [int(row[5])] +code_data(row[6]) + [int(row[7])]
            X.append(sample)
            y.append(mymap[row[8]])
    # clf = tree.DecisionTreeClassifier()
    # clf = clf.fit(X, y)
     # 创建一个预处理和分类的pipeline
    pipeline = make_pipeline(StandardScaler(), tree.DecisionTreeClassifier())

    # 定义要搜索的参数
    param_grid = {'decisiontreeclassifier__max_depth': [3, 5, 7, 10, 15, 20],
                  'decisiontreeclassifier__min_samples_split': [2, 5, 10, 15, 20, 30]}

    # 使用网格搜索和交叉验证
    clf = GridSearchCV(pipeline, param_grid, cv=5)
    clf = clf.fit(X, y)
    return clf


def train_GNB(data):
    X = []
    y = []
    for row in data:
        if int(row[1]) - int(row[2]) <= 10:
            sample = eval(row[4]) + eval(row[5])
            X.append(sample)
            y.append(int(row[3]))
    clf = GaussianNB()
    clf = clf.fit(X, y)
    return clf

def train_SVM(data):
    X = []
    y = []
    for row in data:
        if int(row[1]) - int(row[2]) <= 10:
            sample = eval(row[4]) + eval(row[5])
            X.append(sample)
            y.append(int(row[3]))
    clf = svm.SVC(probability=True)
    clf = clf.fit(X, y)
    return clf

def train_random_forest(data):
    X = []
    y = []
    for row in data:
        if int(row[1]) - int(row[2]) <= 25:
            sample = eval(row[4]) + eval(row[5]) + code_data(row[6])
            X.append(sample)
            y.append(int(row[3]))
    # 创建一个预处理和分类的pipeline
    pipeline = make_pipeline(StandardScaler(), RandomForestClassifier())

    # 定义要搜索的参数
    param_grid = {'randomforestclassifier__n_estimators': [10, 50, 100],
                  'randomforestclassifier__max_depth': [None, 5, 10],
                  'randomforestclassifier__min_samples_split': [2, 5, 10]}

    # 使用网格搜索和交叉验证
    clf = GridSearchCV(pipeline, param_grid, cv=5)
    clf = clf.fit(X, y)
    return clf

def train_combat_forest(data):
    X = []
    y = []
    mymap = {'combat':0, 'bomb':1, 'pass':2}
    for row in data:
        if int(row[1]) - int(row[2]) <= 25 and row[8] != 'best':
            sample = eval(row[3]) + eval(row[4]) + [int(row[5])] +code_data(row[6]) + [int(row[7])]
            X.append(sample)
            y.append(mymap[row[8]])
    # 创建一个预处理和分类的pipeline
    pipeline = make_pipeline(StandardScaler(), RandomForestClassifier())

    # 定义要搜索的参数
    param_grid = {'randomforestclassifier__n_estimators': [10, 50, 100],
                  'randomforestclassifier__max_depth': [None, 5, 10],
                  'randomforestclassifier__min_samples_split': [2, 5, 10]}

    # 使用网格搜索和交叉验证
    clf = GridSearchCV(pipeline, param_grid, cv=5)
    clf = clf.fit(X, y)
    return clf

def save_model(clf, filename):
    dump(clf, filename)

def train():
    data = read_data(data_name)
    # clf = train_GNB(data)
    # clf = train_SVM(data)
    clf = train_decision_tree(data)
    # clf = train_random_forest(data)
    # clf = train_combat_forest(data)
    # clf = train_combat_tree(data)
    save_model(clf, model_name)

if __name__ == '__main__':
    train()