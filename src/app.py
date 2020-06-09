import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template,request
# from predict import prediction
app = Flask(__name__)
options = {
    'Department':['EST','PM','SP'],
    'Union':['OC','Other'],
    'Bid Type':["Select Bid List", "Competitive", "Budget", "Negotiated"],
    'Design Type':['D/A', 'D/B', 'Engineered'],
    'Bid': ['x< $4,520','x< $18,000','x< $116,011', 'x>= $116,011']
    
}
with open('models/randomforest.pkl', 'rb') as f:
    model = pickle.load(f)
with open('models/column_list.pkl', 'rb') as f:
    columns = pickle.load(f)





@app.route('/')
def get_new_data():
    return render_template('input.html', q = options)

@app.route('/prediction', methods=['POST'])
def predict():
    inputs=[]
    for i in options:
        inputs.append(request.form[i])
    df = pd.DataFrame(0, index=np.arange(1), columns=columns)
    if inputs[0]== 'EST':
        df.at[0,'EST']=1
    elif inputs[0]== 'PM':
        df.at[0,'PM']=1

    if inputs[1]== 'OC':
        df.at[0,'OC']=1
   
    if inputs[2]== 'Budget':
        df.at[0,'Budget']=1
    elif inputs[2]== 'Competitive':
        df.at[0,'Competitive']=1
    elif inputs[2]== 'Negotiated':
        df.at[0,'Negotiated']=1    

    if inputs[3]== 'D/A':
        df.at[0,'D/A']=1
    elif inputs[3]== 'D/B':
        df.at[0,'D/B']=1        
    
    if inputs[4]== 'x< $18,000':
        df.at[0,'50% Bid']=1
    elif inputs[4]== 'x< $116,011':
        df.at[0,'75% Bid']=1      
    elif inputs[4]== 'x>= $116,011':
        df.at[0,'Big Bid']=1     
        

    prob = model.predict_proba(df)[:, 1]
    return '<h1>Probability of bid being awarded: <u>'+str(prob)+ str(inputs)+'</u></h1>'
   
    # prob = prediction(X_n)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)