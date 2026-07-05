import numpy as np
import pandas as pd
import mysql.connector
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine


conn = mysql.connector.connect(
    host="localhost",        
    user="root",             
    password="Root@12345",
    database="fake"
)

df = pd.read_sql("select * from Product_Features", conn)
print(df.head())
print(df.info())
print(df.isnull().sum())

X = df[
    [
        'Actual_Market_Price',
        'Listed_Price',
        'Rating',
        'Reviews_Count',
        'Seller_Score'
    ]
]

from sklearn.cluster import DBSCAN
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('dbscan', DBSCAN(
        eps=1.0,
        min_samples=5
    ))
])

clusters = pipeline.fit_predict(X)

df['Cluster'] = clusters

df['Status'] = np.where(
df['Cluster'] == -1,'Suspicious','Genuine')

output = df[
[
'Product_ID',
'Product_Name',
'Actual_Market_Price',
'Listed_Price',
'Rating',
'Reviews_Count',
'Seller_Score',
'Status'
]
]

print(output.sample(10))
print(output['Status'].value_counts())

engine = create_engine(
"mysql+pymysql://root:@12345@localhost/fake"
)

output.to_sql(
name='product_status',
con=engine,
if_exists='replace',
index=False
)

print("\nData Saved  product_status Table")








