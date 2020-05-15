import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
#Creates dataframe frome file
def load_bid_log(file,skip = True):
    
    s = file[5:10]
    if skip:
        df_raw = pd.read_csv(file)
    else:
        df_raw = pd.read_csv(file,skiprows =0)
    # df.info()

    df = df_raw.copy()
    if skip:
        df =df[['Project Name','Project Description','City','Local','Project Type','Bid Type','Design Type','Estimator','DEPT',' Base Bid ','Bid Status']]
    else:
        df =df[['Project Name','Project Description','City','Local','Project Type','Bid Type','Design Type','Estimator','DEPT','  Base Bid  ','Bid Status']]
    is_NaN = df.isnull()
    row_has_NaN = is_NaN.any(axis=1)
    rows_with_NaN = df[row_has_NaN]
#     print(rows_with_NaN)
    return df,s
#cleans dataframe for featurization 
def pipe(df,s, f = False):
    df.dropna(inplace =True)
    
        
    df.drop(df[df['Bid Status']== 'Not Bid'].index,inplace =True)
    if f:
        df.drop(df[df['  Base Bid  ']== '-'].index,inplace =True)
        df['  Base Bid  ']=(df['  Base Bid  '].str.strip('$ \n'))
        df['  Base Bid  ']= df['  Base Bid  '].apply(lambda x: int(x.replace(',','')))
        df[' Base Bid '] = df['  Base Bid  ']
        df.drop(['  Base Bid  '],axis = 1, inplace = True)
    else:
        df.drop(df[df[' Base Bid ']== '-'].index,inplace =True)

        df[' Base Bid ']=(df[' Base Bid '].str.strip('$ \n'))
        df[' Base Bid ']= df[' Base Bid '].apply(lambda x: int(x.replace(',','')))
    
    tit= s + 'Pandas Profiling Report'
    print(tit)
    return  ProfileReport(df, title=tit, html={'style':{'full_width':True}}), df    
#read and clean files 
if __name__ == '__main__':
    yearly_bid_data=[]
    yearly_profiles=[]
    files = ['data/2015 Bid Log.csv','data/2016 Bid Log.csv','data/2017 Bid Log.csv','data/2018 Bid Log.csv','data/2019 Bid Log.csv',]
    
    for file in files:
        df, s = load_bid_log(file,False)
        profile,data = pipe(df,s,True)
        yearly_bid_data.append(data)
        yearly_profiles.append(profile)

    bid_data = pd.concat(yearly_bid_data)

    bid_data['Bid Status'].replace({'Unknown': 'Lost'},inplace = True)
    
    model_data = bid_data[(bid_data['Bid Status'] =='Awarded')|(bid_data['Bid Status'] =='Lost')]
    model_data.to_csv('data/bid_data.csv')
    