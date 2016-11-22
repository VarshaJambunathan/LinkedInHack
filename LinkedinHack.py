
# coding: utf-8

# In[166]:

import pandas as pd
import numpy as np
get_ipython().magic(u'pylab inline')
import matplotlib.pyplot as plt
import csv
import pprint
import seaborn as sns

#jobs_data = pd.read_csv('jobs.tsv',sep='\t')
skill_data = pd.read_csv('skill_ms_dos.csv')
users_data = pd.read_csv('users.tsv',sep='\t')
#users_to_job = pd.read_csv('user-to-job-applications.tsv',sep='\t')


# In[154]:

print skill_data.info()
print users_data.info()
#print users_to_job.info()

#users_data.groupby('Country').count()["UserID"]
#users_to_job.groupby('UserID').count()


# In[155]:

#cleaning the data
#fixing the multivalued fields by converting them to a python list

def fix_field(field):
    
    list_data = []
    # YOUR CODE HERE
    if field.startswith('{'):
        field = field[1:-1]
        list_data = field.split('|')
    elif field == "NULL":
        list_data=[]
    else:
        list_data.append(field)
    return list_data

def process_file(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "SKILLS" in line :
                line["SKILLS"] = fix_field(line["SKILLS"])
            if "FEATURES_USED" in line:
                line["FEATURES_USED"] = fix_field(line["FEATURES_USED"])
            data.append(line)
    return data


# In[156]:

#calling the function to clean the data and displaying a sample output after cleaning
data = process_file('skill_ms_dos.csv')
pprint.pprint(data[0])


# In[157]:

features = ['CONNECTIONS','LEARNING','BUSINESS SERVICE','FOLLOW','SHARE','JOBS AND INTERNSHIPS']
features_data = {}
total_users = len(data)
for feature in features:
    count = 0
    for i in range(0, len(data)):
        if feature in data[i]["FEATURES_USED"]:
            count += 1
    features_data[feature] = (float(count)/total_users)*100  #calculate % users of a particular feature
pprint.pprint(features_data)


# In[312]:

#plot a bar graph for features data

fig = plt.figure(1, figsize=(8, 8))
plt.bar(range(len(features_data)), features_data.values(), align='center')
plt.xticks(range(len(features_data)), features_data.keys(),rotation=70)
fig.suptitle('Features used by linkedIn users', fontsize=20)
plt.xlabel('Features', fontsize=18)
plt.ylabel('Usage Measure in %', fontsize=16)
subplots_adjust(bottom=0.32)
fig.savefig('features_plot.jpg')


# In[170]:

users_data = pd.read_csv('users.tsv',sep='\t')
total = users_data.count()

def modify_data(field):
    users_data[field].replace(to_replace=['Yes','No'],value=[1,0],inplace = True)
    users_data[field].fillna(value=0,inplace = True)

modify_data('CurrentlyEmployed')
modify_data('ManagedOthers')

working_professionals = (users_data['CurrentlyEmployed'].sum() / total['UserID']) *100
managers = (float(users_data['ManagedOthers'].sum()) / total['UserID']) *100


# In[311]:

fig = plt.figure(1, figsize=(8, 8))
a = users_data.groupby('TotalYearsExperience').count()['UserID']
plt.plot(a)
pylab.xlim([0,40])
fig.suptitle('Features used by linkedIn users', fontsize=20)
plt.xlabel('Years of Experience', fontsize=18)
plt.ylabel('Number of users', fontsize=16)
subplots_adjust(bottom=0.16)
fig.savefig('experience_plot.jpg')

#plt.plot(users_data.groupby('TotalYearsExperience').count()['UserID'])
#plt.hist(users_data.groupby('TotalYearsExperience').count()['UserID'],bins=5)


# In[255]:

pprint.pprint(data[0])


# In[287]:

#CONSIDERING ONLY COMPUTER SCIENCE AS INTEREST OPTION 
field_tools = {}
field_tools['ARTIFICIAL INTELLIGENCE']={}
field_tools['DATA SCIENCE'] = {}
field_tools['BIG DATA'] = {}
field_tools['INTERNET OF THINGS'] = {}

#pprint.pprint(field_tools)

for i in range(0,len(data)):
    for tool in data[i]['SKILLS']:
        field = data[i]['FIELD'] 
        #print field_tools[field]
        if bool(field_tools[field]): #if dictionary is empty
            field_tools[field][tool] = 1
        elif tool in field_tools[field]:
            field_tools[field][tool] += 1
        else:
            field_tools[field][tool] = 1
pprint.pprint(field_tools)


# In[ ]:



