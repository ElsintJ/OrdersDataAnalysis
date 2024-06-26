#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install kaggle


# In[2]:


pip install pandas


# In[3]:


#download dataset using kaggle api
import kaggle
get_ipython().system('kaggle datasets download ankitbansal06/retail-orders -f orders.csv')


# In[4]:


#extract file fom zip file
import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip')
zip_ref.extractall()
zip_ref.close()


# In[5]:


#read data fron the file and handle null values
import pandas as pd
df = pd.read_csv('orders.csv',na_values =['Not Available','unknown'])
df.head(20)
df['Ship Mode'].unique()


# In[6]:


#rename column names...make then lowercase and replace space with underscore
#df.rename(columns={'Order Id':'order_id','City':'city'})
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df.head(5)


# In[7]:


#derive new columns discount, sale price and profit
df['discount']=df['list_price']*df['discount_percent']*.01
df['sale_price']=df['list_price']-df['discount']
df['profit']=df['sale_price']-df['cost_price']
df


# In[8]:


#convert order date from object datatype to date time
#df.dtypes
df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")


# In[9]:


#drop cost price, list price and discount percent columns(inplace modifies the original df,otherwise we get back a copy)
#df.dtypes
df.drop(columns=['list_price','cost_price','discount_percent'],inplace=True)


# In[10]:


#load data into sql server using replace option
#df
import sqlalchemy as sal
engine = sal.create_engine('mssql://LAPTOP-HPOEBSFK\SQLEXPRESS/master?driver=ODBC+DRIVER+17+FOR+SQL+SERVER')
conn=engine.connect()


# In[15]:


#Load the data into sql server using append option
#df.to_sql('df_orders',con=conn, index=False, if_exists ='replace')
#But if u use 'replace',pandas create table with highest possible datatypes like bigint,varchar(max) etc.
df.to_sql('df_orders',con=conn, index=False, if_exists ='append')


# In[14]:


df.columns

