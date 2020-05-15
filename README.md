# Bid Modeling

# Background
This data comes from a commercial electrical contractor that specializes in office and medical buildings. In order to get a new project, this company must submit a bid to the general contractor stating the estimated price to complete the job (includes labor, cost of materials, overhead, etc.).

# Goal 
The of this project is to:
      Build a model that can accurately predict whether a project will be awarded or not 
      Determine the factors that affect/affect the result of the bid.

# Data
The data comes from a spreadsheet maintained by a team of estimators. Once an estimator starts a bid, they enter basic information to the spreadsheet. After the estimator has submitted the bid, they update the spreadsheet and set the `Bid_Status` to `Pending`. The spreadsheet is updated again after the bid has been awarded or lost. This is the ideal situation, in reality the spreadsheet is not maintained perfectly. 

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

Accuracy Score: 0.8289473684210527

Recall Score: 0.8006230529595015

Feature |  Coefficient |
| ----------- | ----------- |
| EST | -1.141563 |
| PM | -0.145808 |
| OC | 0.630806 |
| Budget | -0.302537 |
| Competitive | -0.824628 |
| Negotiated | 2.143627 |
| D/A | 0.028728 |
| D/B | 0.750628 |
| 50% Bid | -0.138291 |
| 75% Bid | -0.508384 |
| Big Bid | -0.942494 |

# Conclusion

This model was able to predict whether or not a bid will be awarded fairly well. I was also able to find some relationships between the features and this prediction. I think one of the main weaknesses of this model is lack of data. I plan on trying to update these bid logs in order to fill in missing values and correctly reclassify some of projects that are no longer `Pending`.




