#!/usr/bin/env python
# coding: utf-8

# ## Project Number 3

# ### Data Analyst Expert Course 9297/8

# ### Name: Daniel Rodan

# ##### Stack Exchange Data Analysis

# ###### Importing Libraries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np


# ###### Loading the Data

# In[2]:


users = pd.read_csv(filepath_or_buffer = r'C:\python files\Users.csv',
                    delimiter = ',',
                    header = 0,
                    names = ['Id', 'Reputation', 'CreationDate', 'DisplayName', 'LastAccessDate', 'WebsiteUrl',
                            'Location', 'Age', 'AboutMe', 'Views', 'UpVotes', 'DownVotes'],
                    dtype = {'Id':int, 'Reputation':int, 'DisplayName':str, 'WebsiteUrl':str, 'Location':str,
                            'Age':float, 'AboutMe':str, 'Views':int, 'UpVotes':int, 'DownVotes':int},
                    index_col = 'Id',
                    parse_dates = ['CreationDate', 'LastAccessDate'])


# In[3]:


users.head()


# In[4]:


votes = pd.read_csv(filepath_or_buffer = r'C:\python files\votes.csv',
                   delimiter = ',',
                    header = 0,
                    names = ['Id', 'PostId', 'CreationDate', 'UserId'],
                    dtype = {'Id':int, 'PostId':int, 'UserId':int},
                    index_col = 'Id',
                    parse_dates = ['CreationDate'])


# In[5]:


votes.head()


# In[6]:


comments = pd.read_csv(filepath_or_buffer = r'C:\python files\comments.csv',
                      delimiter = ',',
                      header = 0,
                      names = ['Id', 'PostId', 'Text', 'CreationDate', 'UserId'],
                      dtype = {'Id':int, 'PostId':int, 'Text':str, 'UserId':int},
                      index_col = 'Id',
                      parse_dates = ['CreationDate'])


# In[7]:


comments.head()


# In[8]:


posts = pd.read_csv(filepath_or_buffer = r'C:\python files\Posts.csv',
                    delimiter = ',',
                    header = 0,
                    names = ['Id', 'CreationDate', 'Score', 'ViewCount', 'Body', 'OwnerUserId',
                            'LastEditorUserId', 'LastEditDate', 'LastActivityDate', 'Title', 'Tags', 'ClosedDate'],
                    dtype = {'Id':int, 'Score':int, 'ViewCount':str, 'Body':str, 'OwnerUserId':int,
                            'LastEditorUserId':int, 'Title':str, 'Tags':str},
                    index_col = 'Id',
                    parse_dates = ['CreationDate', 'LastEditDate', 'LastActivityDate', 'ClosedDate'])


# In[9]:


posts.head()


# ##### Basic Analysis

# ###### Ex 1

# In[10]:


mask = posts['CreationDate'].dt.year
df = posts.groupby(mask)['Title'].count().to_frame()
df


# ###### Ex 1 Visualization

# In[11]:


mask = posts['CreationDate'].dt.year.astype(str)
df = posts.groupby(mask)['Title'].count().to_frame()

x_axis = df.index
y_axis = df['Title']

plt.bar(x_axis , y_axis, color = 'darkred', width = 0.6, edgecolor ='black')

plt.grid(b = True, color ='darkred', 
         linestyle ='-.', linewidth = 0.4, 
         alpha = 0.5) 

plt.xlabel('<--- Year --->', fontweight = 'bold', color = 'darkred')
plt.ylabel('<--- Number of Posts --->', fontweight = 'bold', color = 'darkred')
plt.title('Total Posts per Year', loc = 'left', fontweight = 'bold', color = 'darkred', fontsize = 17)

plt.show()


# ###### Ex 2

# In[12]:


mask = votes['CreationDate'].dt.strftime("%A")
votes.groupby(mask)['UserId'].count().to_frame().sort_values('UserId', ascending = False).rename(columns = {'UserId':'TotalVotes'})


# ###### Ex 2 Visualization

# In[13]:


mask = votes['CreationDate'].dt.strftime("%A")
df = votes.groupby(mask)['UserId'].count().to_frame().sort_values('UserId', ascending = False).rename(columns = {'UserId':'TotalVotes'})

df.reset_index(drop = False, inplace = True)

df['Lable'] = df['CreationDate'] + ': ' + df['TotalVotes'].astype(str)

p_size = df['TotalVotes']
p_labels = df['Lable']
p_colors = ['maroon', 'brown', 'indianred', 'lightcoral', 'salmon', 'lightsalmon', 'mistyrose']

plt.pie(p_size, colors = p_colors, labels = p_labels, startangle = 60, explode = (0.1,0.1,0.1,0.1,0.1,0.1,0.1),
       autopct = '%.f%%')

plt.title('Votes per Day of Week', loc = 'left', fontweight = 'bold', color = 'darkred', fontsize = 17)
plt.axis('equal')
plt.show()


# ###### Ex 3

# In[14]:


comments['CreationDate'] = pd.to_datetime(comments['CreationDate'])
mask = (comments['CreationDate'] > '2012-09-19') & (comments['CreationDate'] < '2012-09-20')
comments[mask]


# ###### Ex 4

# In[15]:


mask_null     = users['Location'].notnull() & users['Age'].notnull()
mask_age      = users['Age'] < 33
mask_location = users['Location'].str.contains('London')
users[mask_null & mask_age & mask_location]


# ##### Advanced Analysis

# ###### Ex 1

# In[16]:


x = posts.merge(votes,
               how = 'left',
               left_index = True,
               right_on = 'PostId')

x.groupby('Title')['PostId'].count().to_frame().rename(columns = {'PostId':'Total_Votes'}).sort_values('Total_Votes', ascending = False)


# ###### Ex 2

# In[27]:


join_1 = posts.merge(comments,
                    how = 'inner',
                    left_index = True ,
                    right_on = 'PostId')[['Title', 'OwnerUserId', 'UserId']]

join_2 = join_1.merge(users,
                     how = 'inner',
                     left_on = 'OwnerUserId',
                     right_index = True)[['Title', 'OwnerUserId', 'UserId', 'Location']]\
.rename(columns = {'Location':'Post_Creator_Location'})

join_3 = join_2.merge(users,
                     how = 'inner',
                     left_on = 'UserId',
                     right_index = True)[['Title', 'OwnerUserId', 'UserId','Post_Creator_Location','Location']]\
.rename(columns = {'Location':'Comment_Creator_Location'})

mask = join_3['Post_Creator_Location'] == join_3['Comment_Creator_Location']
join_3[mask]


# ###### Ex 3

# In[39]:


join = users.merge(votes,
                  how = 'left',
                  left_index = True,
                  right_on = 'UserId')

mask = join['PostId'].isnull()
join[mask]['UserId'].count()


# ###### Ex 4

# In[63]:


join = posts.merge(comments,
                  how = 'inner',
                  left_index = True,
                  right_on = 'PostId')\
.groupby('Title')['Title'].count()\
.sort_values(ascending = False)\
.to_frame()\
.rename(columns = {'Title':'Number_of_Comments'})

join


# ###### Ex 5

# In[76]:


join_1  = posts.merge(votes,
                     how = 'inner',
                     left_index = True,
                     right_on = 'PostId')

join_2 = join_1.merge(users,
                     how = 'inner',
                     left_on = 'UserId',
                     right_index = True)\
[['Title', 'Location']]

x = ~join_2['Location'].isnull()
join_2 = join_2[x]

world_votes = join_2.groupby('Title')['Location'].count().to_frame().rename(columns = {'Location':'World_Number_of_Votes'})

mask = join_2['Location'].str.contains('Canada')
canada_votes = join_2[mask].groupby('Title')['Location'].count().to_frame().rename(columns = {'Location': 'Canada_Number_of_Votes'})

join_3 = world_votes.merge(canada_votes,
                          how = 'left',
                          left_index = True,
                          right_index = True)

join_3['Canada_Number_of_Votes'].fillna(value = 0, inplace = True)

join_3['Percentage'] = round((join_3['Canada_Number_of_Votes'] / join_3['World_Number_of_Votes']) * 100)

join_3                    


# ###### Ex 6

# In[80]:


mask = comments.groupby('PostId')['CreationDate'].min().to_frame()

join = posts.merge(mask,
                  how = 'inner',
                  left_index = True,
                  right_index = True)[['Title', 'CreationDate_x', 'CreationDate_y']]\
.rename(columns = {'CreationDate_x': 'Post_CreationDate','CreationDate_y': 'Comment_CreationDate'})

join['hours_number'] = (join['Comment_CreationDate'] - join['Post_CreationDate']) / np.timedelta64(1, 'h')
np.round(join['hours_number'].mean())


# ###### Ex 7

# In[89]:


arr_1 = list(posts['Tags'].str.split('><'))
arr_2 = []

for i in arr_1:
    for j in i:
        arr_2.append(j)

my_df = pd.Series(arr_2).str.replace('>', "").str.replace('<', "").to_frame()
my_df.columns = ['Tag']
my_df.groupby('Tag')['Tag'].count().sort_values(ascending = False).to_frame().rename(columns = {'Tag': 'Number_of_Tags'}).head(1)


# ###### Ex 8

# In[94]:


posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts['Month_Creation'] = posts['CreationDate'].dt.month
posts['Year_Creation'] = posts['CreationDate'].dt.year

posts.pivot_table(index = 'Year_Creation',
                  columns = 'Month_Creation',
                  values = 'Title', 
                  aggfunc = 'count')

