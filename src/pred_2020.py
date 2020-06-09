import pickle
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # read data
    df_raw = pd.read_csv('notebooks/bid2020.csv')
    df = pd.read_csv('data/bid_data2020_feature.csv')
    df.drop(['Unnamed: 0'],axis =1 ,inplace = True)
  
    
    X = df.drop(['Bid Status'],axis = 1)
    
    with open('models/randomforest.pkl', 'rb') as f:
        model = pickle.load(f)

    bids = df_raw[' Base Bid ']                                                                                                                                        
    probs = model.predict_proba(X)[:,1]
    projection = bids*probs
    cum_bids = sum(bids)
    cum_proj = sum(projection)
    print(cum_bids)
    print(cum_proj/cum_bids)