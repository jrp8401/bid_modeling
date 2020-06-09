import numpy as np 
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split, cross_validate,RandomizedSearchCV,GridSearchCV
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.metrics import mean_squared_error,accuracy_score, recall_score, confusion_matrix, roc_auc_score,roc_curve
import matplotlib.pyplot as plt
import pickle
from joblib import dump

def roc(fpr,tpr,auc):
    # Plot the ROC curve
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='k',
            label='Luck')
    ax.plot(fpr, tpr, color='b', lw=2, label='Model')
    ax.set_xlabel("False Positive Rate", fontsize=20)
    ax.set_ylabel("True Postive Rate", fontsize=20)
    ax.set_title("ROC curve", fontsize=24)
    ax.text(0.3, 0.7, " ".join(["AUC:",str(auc.round(3))]), fontsize=20)
    ax.legend(fontsize=24)
    # plt.show()
    plt.savefig('imgs/rf_roc.png')

def VIF(X):
    # Prints VIF for features
    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["features"] = X.columns
    print(vif)


def recll_thres(y_test,probs):

    max_rec = [-1,-1]
    for i in np.arange(.4,.9,.01):
        y_hat = (probs >= i).astype(int)
        rec = (recall_score(y_test, y_hat))
        if rec>max_rec[1]:
            max_rec[0] = i
            max_rec[1] = rec
    print(max_rec[0])
    y_hat = (probs >= max_rec[0]).astype(int)

    return y_hat

def print_scores(y_test,yhat,probs):
    print(recall_score(y_test, yhat)) 
    print(accuracy_score(y_test, yhat))
    print(confusion_matrix(y_test, yhat))
    # print(roc_auc_score(y_test, probs))
    print()

def eval_models(X,y):
    X_train, X_test, y_train, y_test =train_test_split(X,y,random_state = 125,stratify=y)
    #logistic reg
    model = LogisticRegression(n_jobs = -1, tol  = .001, solver = 'liblinear', max_iter = 1000, fit_intercept= True, C=1)  
    model.fit(X_train, y_train)
   
    probs = model.predict_proba(X_test)[:,1]
    yhat = recll_thres(y_test,probs)
    # yhat = model.predict(X_test)
    print_scores(y_test,yhat,probs)

    # print coefs
    print(dict(zip(X.columns,model.coef_[0])))
    print()
    #SGD
    est= SGDClassifier(n_jobs =-1,early_stopping = True,fit_intercept=True, shuffle = True, tol = None, penalty ='l2', max_iter = 1000, loss = 'modified_huber', learning_rate = 'constant', eta0 =.001)
    est.fit(X_train,y_train)
   
    probs = est.predict_proba(X_test)[:,1]
    yhat = recll_thres(y_test,probs)
    # yhat = est.predict(X_test)
    print_scores(y_test,yhat,probs)
    #RandomFOresst
    rf = RandomForestClassifier(n_estimators = 45,min_samples_split = 5,min_samples_leaf = 4,max_features = 'sqrt', max_depth = 52)
    rf.fit(X_train,y_train)

    probs = rf.predict_proba(X_test)[:,1]
    yhat = recll_thres(y_test,probs)
    # yhat = rf.predict(X_test)
    print_scores(y_test,yhat,probs)

def dump_model(rf, train_columns):
    with open('models/randomforest.pkl', 'wb') as f:
        pickle.dump(rf, f)
    
    with open('models/column_list.pkl', 'wb') as f:
        pickle.dump(train_columns, f)
    dump(rf, 'models/randomforest.joblib')

if __name__ == '__main__':
    # read data
    df = pd.read_csv('data/bid_data_feature2.0.csv')
    df.drop(['Unnamed: 0'],axis =1 ,inplace = True)
  
    y = df['Bid Status']
    X = df.drop(['Bid Status'],axis = 1)
    # VIF(X)
    eval_models(X,y)
   
    rf = RandomForestClassifier(n_estimators = 45,min_samples_split = 5,min_samples_leaf = 4,max_features = 'sqrt', max_depth = 52)
    rf.fit(X, y)
    train_columns = list(X.columns)
    
    dump_model(rf, train_columns)
   