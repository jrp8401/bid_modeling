from joblib import load
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

model = load("models/randomforest.pkl")
col = load('models/column_list.pkl')
importances = model.feature_importances_
std = np.std([tree.feature_importances_ for tree in model.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
# print("Feature ranking:")
feature_names = col

# for f in range(10):
#     print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# sorted(zip(map(lambda x: round(x,4), model.steps[1][1].feature_importances_),  

important_features = pd.Series(data=importances,index=feature_names)
important_features.sort_values(ascending=False,inplace=True)
important_features.nlargest(12).plot(kind = 'barh')
plt.title("Top important features")
plt.savefig('imgs/feat_import.png')

# plt.figure()
# plt.title("Feature importances")
# plt.bar(range(12), importances[indices],
#         color="r", yerr=std[indices], align="center")
# plt.xticks(range(12), indices)
# plt.xlim([-1, 12])
# plt.show()