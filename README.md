# bid_modeling

Background
This data comes from a comercial electrical contractor that specializes in office and medical buildings. In order to get a new project, this company must submit a bid to the general contractor stating the esitmated price to complete the job (includes labor, cost of materials,overhead, etc.).

goal 
The of this project is to:
      Build a model that can accuratly predict whether a project will be awarded or not 
      Determine the factors that efffect/affect the result of the bid.

    

After recieving an invitation to bid from the general contractor, the Cheif estimator decieds to pursue bid, assign to estimator, logs job (est numbr info at time), start doing takeoff/ reuests quotes for proucts/ calculates bid/ submits bid/ sets status to pending/ Chefi follows up with customer, awarde/further negotiated/ monthly review of bid log to update info
sometimes bids get combined hard to track 
jobs may stay pending


Invites/applications from General contracts sends a request for a bid. mostly focus on companies that have prior relatiohsips
some projects are done throgh GCs but other projects have full time electricans working a a facilty where constant presence client.
Come walk job and give an estimate. most work through GC Socal locals
Hospital work/ medical office building/TI/Pharmacuitcal Uninon contractor/ harder to be competitive on smaller to mid range projects
long term relatioships





data
The data comes from a spreadhsheet maintaied by the estimators. Due to this I anticpated the data to have some mistakes and upon my initial EDA I noticed emppty values in the spreadsheet. I was able to fill out some missign data based on other information in the spreadsheet The features that were availible for almost every project was Project Description, City, Electricans Guild, Project Type, Bid Type, Design Type, Estimator, Department, Bid amount and the Result of the bid. 

EDA
Upon my initial look at the spreadsheets I quicky realized of the 50 columns only 11 were comeplete enough to be useful. Even after narrowing it down to these features there were still some missing data. I was able 

combined 5 years of bid logs
In the `Bid Status` the possible values include `Awarded`, `Lost` or `Pending`. 
Data upkeep
ennded up dropping about 1/4 of the projects from the data becuase I was uncertain on the result of the bid


Base bid bistograms
most of the bids are small projects, these projects have a high hit rate

medium range

big bids lower hit rate


department ratios
SP is most of these cheap projects usually from existsig 
est more of the compet bids

Bid types
    comp more comp 
    select bid list most common 
    negoitated solid
        both working wiht previous relationships

Local refers to the local electricians guild. 
    most jobs in OC
    Bids in other counties dont go so well


Featurized


Cleaning pipeline

Modeling

Results
