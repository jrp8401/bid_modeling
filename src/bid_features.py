
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # read cleanded data
    df_train = pd.read_csv('notebooks/bid_data2.0.csv')
    df_raw = pd.read_csv('notebooks/bid2020.csv')
    df_raw1=df_raw.copy()
    df_raw.drop(['Unnamed: 0','City','Project Type','Estimator','Project Name'],axis = 1,inplace =True)

    # dept featurize
    df_raw["Department: Estimating"] = df_raw.DEPT.map( lambda x: 1.0 if x==' Est. ' else 0.0 )
    df_raw["Department: Project Managers"] = df_raw.DEPT.map( lambda x: 1.0 if x==' P.M. ' else 0.0 )
    # df_raw["SP"] = df_raw.DEPT.map( lambda x: 1.0 if x==' S.P. ' else 0.0 )

    df_raw.drop(['DEPT'], axis = 1, inplace = True)

    # Local featurize
    df_raw["Orange County"] = df_raw.Local.map( lambda x: 1.0 if x==' 441 OC ' else 0.0 )
    # df_raw["LA"] = df_raw.Local.map( lambda x: 1.0 if x== ' 11 LA ' else 0.0 )
    # df_raw["NonOC/LA"] = df_raw.Local.map( lambda x: 1.0 if ((x==' 440 RS ') or  (x==' 477 SB ') or (x==' 401 Reno '))  else 0.0 )

    df_raw.drop(['Local'], axis = 1, inplace = True)

    # Bid Type
    # df_raw["Select"] = df_raw['Bid Type'].map( lambda x: 1.0 if x==' Select Bid List 'else 0.0 )
    df_raw["Budget Bid"] = df_raw['Bid Type'].map( lambda x: 1.0 if x==' Budget 'else 0.0 )
    df_raw["Competitive Bid"] = df_raw['Bid Type'].map( lambda x: 1.0 if x==' Competitive 'else 0.0 )
    df_raw["Negotiated Bid"] = df_raw['Bid Type'].map( lambda x: 1.0 if x==' Negotiated 'else 0.0 )
    df_raw.drop(['Bid Type'], axis = 1, inplace = True)

    # Design Type
    df_raw["Design/Assist"] = df_raw['Design Type'].map( lambda x: 1.0 if x==' Design/ Assist ' else 0.0 )
    df_raw["Design/Build"] = df_raw['Design Type'].map( lambda x: 1.0 if x==' Design/Build ' else 0.0 )
    # df_raw["Engine"] = df_raw['Design Type'].map( lambda x: 1.0 if x==' Engineered ' else 0.0 )
    df_raw.drop(['Design Type'], axis = 1, inplace = True)

    # Base Bid
    stats =df_train[' Base Bid '].describe()
    # df_raw["25% Bid"] = df_raw[' Base Bid '].map( lambda x: 1.0 if x<stats[4] else 0.0 )
    df_raw["50% Bid"] = df_raw[' Base Bid '].map( lambda x: 1.0 if (x>=stats[4]) and (x<stats[5]) else 0.0 )
    df_raw["75% Bid"] = df_raw[' Base Bid '].map( lambda x: 1.0 if (x>=stats[5]) and (x<stats[6]) else 0.0 )
    df_raw["Big Bid"] = df_raw[' Base Bid '].map( lambda x: 1.0 if (x>=stats[6]) else 0.0 )
    df_raw.drop([' Base Bid '], axis = 1, inplace = True)

    # Bid Status
    df_raw["Bid Status"] = df_raw['Bid Status'].map( lambda x: 1.0 if x=='Awarded' else 0.0 )
    df_raw.to_csv('data/bid_data2020_feature.csv')