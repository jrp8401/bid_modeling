# Bid Modeling

# Background
This data set comes from a commercial electrical contractor that specializes in office and medical buildings. In order to get a new project, this company must submit a bid to the general contractor stating the estimated price to complete the job (includes labor, cost of materials, overhead, etc.).

# Goal 
The of this project is to:
      
      Build a model that can accurately predict whether a project will be awarded or not 
      Determine the factors that affect/affect the result of the bid.

# Data
The data comes from a spreadsheet maintained by a team of estimators. When an estimator starts a bid, they enter basic information to the spreadsheet. Once the estimator has submitted the bid, they update the spreadsheet with additional information as well as set the `Bid_Status` to `Pending`. The spreadsheet is updated again after the bid has been awarded or lost. This is the ideal situation, in reality the spreadsheet is not maintained perfectly. 

Upon my initial EDA I noticed empty values in the spreadsheet. I was able to fill out some missing data based on other information in the spreadsheet. The data also had inconsistencies in spelling, spacing and abbreviations so I had to find the outliers and modify some values to create accurate categories. In the 5 years of bid logs there were about 1400 individual bids, however over 500 were still left `Pending`, so I had to drop those data points for now. Several factors contributed to this: breakdown of communication between departments, jobs being cancelled after bids were submitted, jobs that are actually pending (bid not awarded to anyone yet).

# EDA
The features that were available for almost every project was `Project Description`, `City`, `Local Guild`, `Project Type`, `Bid Type`, `Design Type`, `Estimator`, `Department`, `Bid Amount` and `Bid Status`.


![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/base_bid.png)


One of the first features I looked at was the `Bid Amount` in dollars. Most of the bids are on smaller, cheaper projects, however there is a small portion of million dollar plus bids. These cheaper projects have a higher hit rate than the expensive ones. 

**Bid Amount**

![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/low_range.png)

![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/mid_low.png)

![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/high_mid.png)

![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/bid_range.png)



**Departments**

![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/departments.png)

The three different departments tend to bid on specific projects.
Special projects mostly works cheaper projects, usually an update for a past client.  


**Bid Types**

![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/bid_type.png)

Select Bid List refers to the small amount of other electrical contractors bidding for the job. 
While competitive is against several other companies. 

**Local**

![](https://github.com/jrp8401/bid_modeling/blob/master/imgs/local.png)

Since this company is based in Orange County it is unsurprising to see that the majority of the jobs are local. 
Bids outside of OC do not do well. 
 
# Feature Engineering
In order to change `Bid Amount` from a numerical value to a categorical value based on the IQR. Then I created a column for every category in each of the other features. I then performed VIF and removed the feature with the highest score. I repeated this several times to minimize the VIF scores and reduce collinearity between features. I also changed my target `Bid Status` from `Awarded` and `Lost` to `1` and `0`.   


# Models
Since there is an imbalance between the `Awarded` and `Lost` classes I used SMOTE to resample and split my train and test sets.
I then used GridSearchCV along with a LogisticRegression model to choose the optimal parameters for the model. 


Accuracy Score: 0.8006230529595015

Recall Score: 0.8289473684210527



Feature |  Coefficient |
| ----------- | ----------- |
| Bid Type-Negotiated | 0.779 |
| Local-Orange County | 0.284 |
| Dept-Project Managers | 0.146 |
| Design Type-Design/Build | -0.034 |
| Dept-Estimating | -0.204 |
| 25%-50% Bid | -0.305 |
| Design Type-Design/Assist | -0.327 |
| Bid Type-Competitive | -0.476 |
| 50%-75% Bid | -0.637 |
| Bid Type-Budget | -1.062 |
| 75%+ Bid | -1.143 |

# Conclusion

This model was able to predict whether or not a bid will be awarded fairly well. It was also able to find factors that influence the predictions. I think one of the main weaknesses of this model is lack of data. I plan on trying to update these bid logs in order to fill in missing values and correctly reclassify some of projects that are no longer `Pending`.




