#%%[markdown]
#  This is a markdown document created in vscode with `.py` extension

# # Analyzing USCIS case status

# Disclaimer: I am not an attorny, and the information here is in no way supposed to provide legal advice. 
# ## Background

# USCIS receives hundreds (i think) of applications daily and creates an ID for each application it receives called Reciept Number.
# The recipt number is an alphanumeric string of length 13 that starts with 3 letters (denoting the processing center) and 10 digits 
# that are the combinations of fiscal year, computer work day, and serial number (according to the internet).   


# I created a [module]('.\uscis') that takes in the receipt number and returns the heading of the status and the details.
# Then i further used the same module to gather about 4000 cases (before the server blocked my ip). The data is available in the [csv file]("uscis_status.csv")
# and has four columns  

# - downloaded: computer time of downloading
# - receipt: recipt number from USCIS
# - heading: the heading of the case status
# - detail: detail of the case status


# In this project, I will read in data requested for egov.uscis.gov/casestatus.


#%%
# install python modules

# !pip install pandas
# !pip install matplotlib


#%%
#import python modules
import pandas as pd
import sqlite3
from matplotlib.pyplot import plot as plt
%matplotlib inline

#%%
#create sql connection object
con = sqlite3.connect("immigration.db")
df = pd.read_sql_query("select * from casestatus;", con)
print(df.shape)
print(df.head(5))
print(df.dtypes)

#%%[markdown]

# After reading in the data and checking for data type, we need to see how the data is distributed.
# We draw a simple bar graph to understand what current status 
# of most of the application are. To do that, we count the values of each item in heading and plot a 
# bar graph

#%%
#looking at the distribution of headings
print(df['heading'].value_counts().sort_values(ascending=False))

barplot = df['heading'].value_counts().head(10).plot(kind='bar', 
            alpha=.75, figsize=(12,10), color='navy')

#%%[markdown]

# As we can see that for a third of the application, the "card" was delivered 
# (which means the application was approved) and for a sixth, the case was received (they received the application)


# As we can see the useful information are in the `detail` column. It has last activity date, 
# what the deicsion is, etc. We could probably try to get information from the text values. We will need to do some 
# text processing/feature engieering to get the data that we are interested in. Part of the text i am interested in are:
# - Last date the application status was updated (usually for sentence)
# - The form number for the receipt (tells what kind of application it was)
# - Decision (maybe)

#%%
df['last_opened'] = df['detail'].str.extract(r"(\w+ \d{1,2}, \d{4})",0)
df['form'] = df['detail'].str.extract(r"(\w-\d{1,3})",0)


#%%[markdown]

# more plots

#%%
pie= df['form'].dropna().value_counts().plot(kind='pie')


#%%[markdown]

# We can see that the four forms I-130, I-131, I-485, and I-765 are in almost equal proportion.
# It makes sense that those four fomrs are in equal proportions since USCIS National Benefits center, 
# where receipt numbers start with MSC, receives permanent resicency applications along with petition for relative.
# Usually, each petitioner files all these forms together 

# In addition there are other forms which are in very small proportions as well. Which aren't very informative.
# The employment authorization documents and Advance Parole Documents usually get approved within a few months wherease
# the change of status and forein relative petition takes longer. We can see t

# Close inspection of the form counts and their statuses

#%% 
df[df['form'].isin(['I-130', 'I-131', 'I-485', 'I-765'])].groupby(['form','heading'])['recipt'].count()



#%%[markdown]
# checking the status of form I-485 can explain how the cases are moving. 
# Another way to think about it is that every unique person can be identified 
# by their I-485 number. Once their i-485 is completed/closed, their case is closed

#%% 
greencard = df[df['form']=='I-485']
print(greencard.head())

#%%
import datetime
print(datetime.datetime.now() -df.to_datetime(['last_opened'],format='%B %d, %Y'))
# print(datetime.date.today()- datetime.strptime('February 1, 2019', '%B %d %Y'))


#%%
