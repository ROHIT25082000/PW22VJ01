import pandas as pd
import numpy as np
from numpy import percentile
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from pyod.models.iforest import IForest
from scipy import stats

import os 

print(os.getcwd())
curr_file_path = os.getcwd()
input_base_path = curr_file_path + "/uploads"

output_base_path = curr_file_path + "/downloads"  
os.chdir(input_base_path) 

inputFilename = os.listdir()[0]  
outputFilename = "breach_output_model_1.csv"

print(inputFilename)
os.chdir(curr_file_path)
data = pd.read_csv(input_base_path + "/" + inputFilename)

#Creation of ORDER Dataframe
order = data[data['SHORTNAME_OF_URL'] == 'order']

#Drop the columns which are unnecessary for breach
order = order.drop(['IP','TYPE(GET/POST)','HTTP CODE','IF_LOGGED','URL_LINK','SHORTNAME_OF_URL','EMAIL','CARDNUM','MERCHANT','RATING','ZIPCODE'], axis=1)

#Converting each column into their respective data types
order['DATE']=pd.to_datetime(order['DATE'])
order['USER_ID']=pd.to_numeric(order['USER_ID'])
order['PRODUCT_ID']=pd.to_numeric(order['PRODUCT_ID'])
order['PRICE']=pd.to_numeric(order['PRICE'])
order['QUANTITY']=pd.to_numeric(order['QUANTITY'])

cols = ['PRODUCT_ID', 'QUANTITY']
minQuan=min(order['QUANTITY'])
maxQuan=max(order['QUANTITY'])
QuanRange=(minQuan,maxQuan)
minProd=min(order['PRODUCT_ID'])
maxProd=max(order['PRODUCT_ID'])
ProdRange=(minProd,maxProd)

minmax = MinMaxScaler(feature_range=(0, 1))
minmaxobj = minmax.fit(order[['PRODUCT_ID', 'QUANTITY']])
order[['PRODUCT_ID', 'QUANTITY']] = minmax.fit_transform(order[['PRODUCT_ID', 'QUANTITY']])

X1 = order['PRODUCT_ID'].values.reshape(-1,1)
X2 = order['QUANTITY'].values.reshape(-1,1)

X = np.concatenate((X1,X2),axis=1)

#Isolation Forest
outliers_fraction = 0.01
xx , yy = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
clf = IForest(contamination=outliers_fraction,random_state=0)
clf.fit(X)
# predict raw anomaly score
scores_pred = clf.decision_function(X) * -1
        
# prediction of a datapoint category outlier or inlier
y_pred = clf.predict(X)
n_inliers = len(y_pred) - np.count_nonzero(y_pred)    #no of inliers
n_outliers = np.count_nonzero(y_pred == 1)     #no_of_outliers
# copy of dataframe
out = order
out['outlier'] = y_pred.tolist()

out[['PRODUCT_ID', 'QUANTITY']] = minmaxobj.inverse_transform(order[['PRODUCT_ID', 'QUANTITY']])
out['PRODUCT_ID']=out['PRODUCT_ID'].round()

productidList=out['PRODUCT_ID'].unique()
out['QUANTITY'].mode()
resultDict=dict()
for productid in productidList:
  temp=max(out['QUANTITY'][out['PRODUCT_ID']==productid][out['outlier']==0])
  resultDict[productid]=temp
print(resultDict)

l= out.loc[out['outlier'] == 1].index.values.tolist()
outliers = data[data.index.isin(l)]
outliers.to_csv(output_base_path + "/" + outputFilename)