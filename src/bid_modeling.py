import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,GridSearchCV,RandomizedSearchCV
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import mean_squared_error, balanced_accuracy_score, accuracy_score,accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import statsmodels.api as sm
from imblearn.over_sampling import SMOTE
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from pandas.plotting import table 
import matplotlib.pyplot as plt
def bid_model(X_train,y_train,X_test,y_test,grid, model,log= True):
   
    gridsearch = GridSearchCV(model(), grid, n_jobs = -1)
    gridsearch.fit(X_train, y_train)
    param = gridsearch.best_params_
    print("Best parameters:")
    print()
    print(gridsearch.best_params_)
    if log:
        probs = gridsearch.predict_proba(X_test)[:,1]
        max_acc = [-1,-1]
        for i in np.arange(.2,.8,.01):
            y_hat = (probs >= i).astype(int)
            acc = (accuracy_score(y_test, y_hat))
            if acc>max_acc[1]:
                max_acc[0] = i
                max_acc[1] = acc
        y_hat = (probs >= max_acc[0]).astype(int)
    else:
        y_hat = gridsearch.predict(X_test)
            
        
    
    
    
    print(recall_score(y_test, y_hat)) 
    print(accuracy_score(y_test, y_hat))
    print(confusion_matrix(y_test, y_hat))

    print(dict(zip(X.columns,gridsearch.best_estimator_.coef_[0])))
    return gridsearch.best_estimator_.coef_[0]
    # return accuracy_score(y_test, y_hat),recall_score(y_test, y_hat), param

if __name__ == '__main__':
    # read data
    df = pd.read_csv('data/bid_data_feature.csv')
    df.drop(['Unnamed: 0'],axis =1 ,inplace = True)
  
    y = df['Bid Status']
    X = df.drop(['Bid Status'],axis = 1)
   
    # VIF
    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["features"] = X.columns
    print(vif)

    # SMOTE sampling class imbalance
    X_resampled, y_resampled = SMOTE().fit_resample(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X_resampled,y_resampled)

    results  =[]


    # rf_grid = {"n_estimators": [10, 100, 500],
    #              "max_depth":[5,10,25,None],
    #              "min_samples_leaf":[2,10,50],
    #              "max_leaf_nodes": [2, 5,10]}
   
    # results.append(bid_model(X_train,y_train,X_test,y_test,rf_grid, RandomForestClassifier))
    # random_grid ={'bootstrap': [True, False],
    #                 'max_depth': [10, 20, 50, 100, None],
    #                 'max_features': ['auto', 'sqrt'],
    #                 'min_samples_leaf': [1, 2, 4],
    #                 'min_samples_split': [2, 5, 10],
    #                 'n_estimators': [100,200, 400, 1000]}

    # rf = RandomForestClassifier()
    # rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 50, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    # # Fit the random search model
    # rf_random.fit(X_train, y_train)

    # probs = rf_random.predict_proba(X_test)[:,1]
    # max_acc = [-1,-1]
    # for i in np.arange(.2,.8,.01):
    #     y_hat = (probs >= i).astype(int)
    #     acc = (accuracy_score(y_test, y_hat))
    #     if acc>max_acc[1]:
    #         max_acc[0] = i
    #         max_acc[1] = acc
    # y_hat = (probs >= max_acc[0]).astype(int)
    
    # print(recall_score(y_test, y_hat)) 
    # print(accuracy_score(y_test, y_hat))
    # print(confusion_matrix(y_test, y_hat))

    # print(dict(zip(X.columns,rf_random.best_estimator_.feature_importances_)))

    log_reg_grid = {'C':[1,10,100], 
                'fit_intercept' :[True,False],
                'solver' : ['newton-cg', 'liblinear', 'sag','saga','lbfgs'],
                'max_iter' : [100,500,1000,2000]
                
               }
    coefs= bid_model(X_train,y_train,X_test,y_test,log_reg_grid, LogisticRegression)

    df = pd.DataFrame()
    df['Features'] = X.columns 
    df['Coefs'] = coefs
    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, df)  # where df is your data frame

    plt.savefig('Coefs.png')
    

    # fpr, tpr, thresholds = metrics.roc_curve(y_test, probs, pos_label=1)
    # auc = metrics.roc_auc_score(y_test, probs)

    # # Plot the ROC
    # fig = plt.figure(figsize=(10,8))
    # ax = fig.add_subplot(111)
    # ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='k',
    #         label='Luck')
    # ax.plot(fpr, tpr, color='b', lw=2, label='Model')
    # ax.set_xlabel("False Positive Rate", fontsize=20)
    # ax.set_ylabel("True Postive Rate", fontsize=20)
    # ax.set_title("ROC curve", fontsize=24)
    # ax.text(0.3, 0.7, " ".join(["AUC:",str(auc.round(3))]), fontsize=20)
    # ax.legend(fontsize=24);
    # plt.show()