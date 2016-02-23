
# coding: utf-8

# In[55]:

from __future__ import division
#All the imports together.
import sys
import argparse
import pandas as pd
import numpy as np 
import scipy.stats as ss
import scipy.integrate as si
import matplotlib.pyplot as plt


# In[58]:

#######################################################
#A. Read in the CSV.
#COLUMN HEADERS: All column headers ending in “Value” 
########################################################
file_input = sys.argv[-1]

data= pd.read_csv(file_input)
#df = pd.DataFrame(data)
df= pd.read_csv(file_input)

# filtering out all COUNTYCODE==0  #
data= data[data['COUNTYCODE']!=0]
df=df[df['COUNTYCODE']!=0]

value_columns= [col for col in df.columns if 'Value' in col]
'''
for col in df.columns:
    if 'Value' in col:
        print col
'''
print("(1)COLUMN HEADERS")
print ("*****************")
#print(value_columns)
#data= pd.read_csv("2015_CHR_Analytic_Data.csv", usecols = [col for col in df.columns if 'Value' in col])
#data.head(10)
i=0
for elements in value_columns:
    print "["+ str(i) +"]  "+ elements
    i+=1


# In[59]:

#######################################################
#A. 2. TOTAL COUNTIES IN FILE: The total number of counties in the file. 
########################################################
df_county=df[df['COUNTYCODE']!=0]['COUNTYCODE']  # removing the counties which have aggregated values
print "(2) TOTAL COUNTIES IN FILE:",df_county.count()


# In[60]:

#######################################################
#A. 3.TOTAL RANKED COUNTIES: The total number of counties 
#     without a “1” in the field “County that was not ranked” 
########################################################
 
df_filter=df[df['County that was not ranked'] == 1] #list of counties that were not ranked
df_counties_not_ranked=df_filter['County that was not ranked'].count()


df_counties_ranked=df.shape[0]-df_counties_not_ranked
#print df_counties_not_ranked
#total_ranked_counties=df_counties.count()
print "(3)a.  TOTAL RANKED COUNTIES= ",df_counties_ranked
print "(3)b. TOTAL COUNTIES NOT RANKED= ",df_counties_not_ranked


# In[61]:

#######################################################
#B. 4.HISTOGRAM OF POPULATION: a1_4_histpop.png: A histogram of the field 
#    “'2011 population estimate Value'”. 
#    Choose an appropriate number of bins

########################################################

df_population =data[data['COUNTYCODE']!= 0]['2011 population estimate Value'].replace(to_replace=r',',value=r'', regex=True).astype(int)
df_population=df_population[df_population>0]
df_population.describe()
#df_population.dtypes
#df_population[['min','max']].plot(kind='bar')
print "(4) HISTOGRAM OF POPULATION"
plt.ylabel('Frequency')
plt.xlabel("2011 population estimate Value [70 bins]")
plt.title("(4) HISTOGRAM OF POPULATION [a1_4_histpop.png]")
fig=df_population.plot(kind="hist", bins=70)
#df_population.hist(bins=50)
plt.savefig("a1_4_hispop.png")
plt.close("all")
#df_population.hist(bins=500,alpha=0.5)


# In[62]:

df_log=np.log(df_population)
#######################################################
#B. 4.HISTOGRAM OF POPULATION: a1_4_histpop.png: A histogram of the field 
#    “'2011 population estimate Value'”. 
#    Choose an appropriate number of bins

########################################################
print "(5) HISTOGRAM OF LOG POPULATION : bins=15 "

plt.ylabel('Frequency')
plt.xlabel("log of 2011 population estimate Value [15 bins]")
plt.title("(5) HISTOGRAM OF LOG POPULATION : [bins=15]")
fig=df_log.hist(bins=15)
#df_population.hist(bins=50)
plt.savefig("a1_5_histlog.png")
plt.close("all")

# In[63]:

#######################################################
#B. 5.KERNEL DENSITY ESTIMATES: a1_6_KDE.png: 2 kernel density plots 
#     based on log_pop: (a) counties not ranked, and (b) counties ranked.
#     Overlay the density plots over each other into a single graph. 
#     Zoom in if necessary to see the the non-ranked distribution clearly.
########################################################
df_fillna=data.fillna(0)
#print df_fillna
df_counties_ranked=df_fillna[df_fillna['County that was not ranked'] == 0] #list of counties that were ranked
df_counties_not_ranked=df_fillna[df_fillna['County that was not ranked'] == 1] #list of counties that were ranked

df_log_counties_ranked=np.log(df_counties_ranked['2011 population estimate Value']
                              .replace(to_replace=r',',value=r'', regex=True).astype(int))
df_log_counties_not_ranked=np.log(df_counties_not_ranked['2011 population estimate Value']
                                  .replace(to_replace=r',',value=r'', regex=True).astype(int))

plt.ylabel('Density')
plt.xlabel("LOG[2011 population estimate Value]")
plt.title("(6) KERNEL DENSITY ESTIMATES (green: not ranked, blue : ranked)")
fig=df_log_counties_ranked.plot(kind='kde')
fig=df_log_counties_not_ranked.plot(kind='kde')
plt.savefig("a1_6_KDE.png")
plt.close("all")

#print df_log_counties_ranked.replace(to_replace=r',',value=r'', regex=True).astype(float)
#values = np.zeros(1, dtype=float)
#index = ['Row']
#df = pd.DataFrame(values, index=index)



# In[64]:

#######################################################
#B. 6.PROBABILITY RANKED GIVEN POP: Three probabilities --
#     The estimated probability that an unseen county would be ranked, 
#     given the following (non-logged) populations: 300, 3100, 5000. 
########################################################

#using bayes theorem:
#all_columns= [col for col in df.columns if 'seen' in col]
#print all_columns 
print "(7) PROBABILITY RANKED GIVEN POP:"
data=data.replace(to_replace=r',',value=r'', regex=True)
df_CR=data[data['County that was not ranked'] == 1] #list of counties that were ranked
df_CR_count=df_CR['County that was not ranked'].count()
#print df_CR['2011 population estimate Value']

prob_county_ranked=df_CR.count()
prob_county_ranked_and_300=df_CR[df_CR['2011 population estimate Value'].replace(to_replace=r',',value=r'', regex=True).astype(int) ==300]['2011 population estimate Value'].count()
#print prob_county_ranked_and_300
prob_pop_300=data[data['2011 population estimate Value'] ==300]['2011 population estimate Value'].count()
prob_county_ranked_given_300=prob_county_ranked_and_300/prob_pop_300

print prob_county_ranked_given_300

prob_county_ranked=df_CR.count()
prob_county_ranked_and_300=df_CR[df_CR['2011 population estimate Value'] ==5000]['2011 population estimate Value'].count()
#print "(7) PROBABILITY RANKED GIVEN POP:" 
print prob_county_ranked_and_300
prob_pop_300=data[data['2011 population estimate Value'] ==5000]['2011 population estimate Value'].count()
prob_county_ranked_given_300=prob_county_ranked_and_300/prob_pop_300


# In[65]:

#######################################################
#C. 8.LIST MEAN AND STD_DEV PER COLUMN: For each value column, 
#     output it’s mean and standard deviation according to MLE,
#     assuming a normal distribution (pprint a dictionary of {column: (mean, std-dev), … }). 
########################################################

#df= pd.read_csv("2015_CHR_Analytic_Data.csv")
value_columns= [col for col in df.columns if 'Value' in col]
df_value_columns=df[value_columns]
dict={}
for i in range(0,len(value_columns)):
    mean_t=df_value_columns.iloc[:,[i]].fillna(-99).replace(to_replace=r',',value=r'', regex=True).astype(float)
    mean_1=mean_t[mean_t.iloc[:,[0]]>=0].mean()
    #sd_t= df_value_columns.iloc[:,[i]].fillna(-99).replace(to_replace=r',',value=r'', regex=True).astype(float)
    std_1=mean_t[mean_t.iloc[:,[0]]>=0].std()
    dict[value_columns[i]]=(float(mean_1),float(std_1))
    #print dict[value_columns[i]]
    #print mean1
    #print sd1
print "(8) LIST MEAN AND STD_DEV PER COLUMN:"
print "**************************************"
i=1
for elements in dict:
    print "["+str(i)+"] "+str(elements) +"  ----  "+str(dict[elements])
    i+=1


# In[66]:

#######################################################
#C. 9.PSEUDO-POP-DEPENDENT COLUMNS: List of columns which appear
#      to be dependent on log_pop.  We will discuss standard tests 
#      for independence after discussing hypothesis testing. For the 
#      purposes of this assignment, we will call two continuous random variables,
#      A and B “pseodo-independent” iff  | E(A| B<μB) - E(A| B>μB) | < 0.5*𝜎A.  
#      Although the variables in “value” columns have been normalized by population, 
#      some may still be dependent on population. For example, certain mortality rates are 
#      higher in more rural communities because they are often poorer and have less access to health care. 
#################################################################################


