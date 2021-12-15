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
print() 
outputFilename = "credit_card_fraud_model_3.csv"

print(inputFilename)


df=pd.read_csv(input_base_path +"/" +inputFilename)

df.USER_ID=pd.to_numeric(df.USER_ID,errors='coerce')
df.PRODUCT_ID=pd.to_numeric(df.PRODUCT_ID,errors='coerce')
df.RATING=pd.to_numeric(df.RATING,errors='coerce')
df.CARDNUM=pd.to_numeric(df.CARDNUM,errors='coerce')
df.DATE =pd.to_datetime(df.DATE,errors='coerce')
df.AMOUNT=pd.to_numeric(df.AMOUNT,errors='coerce')

listofcards=df.CARDNUM.unique()
listofcards=listofcards[np.isfinite(listofcards)]
mappings=dict()
count=1
for i in listofcards:
  count+=1
  mappings[i]=count
df=df.dropna(subset=['RATING'])
df.groupby('CARDNUM', as_index=False)['AMOUNT'].mean()
listofzscore=df.groupby('CARDNUM', as_index=False)['AMOUNT'].transform(lambda x : stats.zscore(x,ddof=1))
df.insert(17,"A_ZSCORE",listofzscore)
df['A_ZSCORE']=df['A_ZSCORE'].fillna(0)

cols = ['CARDNUM', 'A_ZSCORE']
moddf=df[cols]
moddf['CARDNUM'].map(mappings)

minQuan=min(moddf['A_ZSCORE'])
maxQuan=max(moddf['A_ZSCORE'])
QuanRange=(minQuan,maxQuan)
minProd=min(moddf['CARDNUM'])
maxProd=max(moddf['CARDNUM'])
ProdRange=(minProd,maxProd)
moddf['A_ZSCORE'].isnull().values.sum()
minmax = MinMaxScaler(feature_range=(0, 1))
minmaxobj = minmax.fit(moddf[['CARDNUM', 'A_ZSCORE']])
moddf[['CARDNUM', 'A_ZSCORE']] = minmax.fit_transform(moddf[['CARDNUM', 'A_ZSCORE']])

X1 = moddf['CARDNUM'].values.reshape(-1,1)
X2 = moddf['A_ZSCORE'].values.reshape(-1,1)
X = np.concatenate((X1,X2),axis=1)

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
out = moddf
out['outlier'] = y_pred.tolist()

out[['CARDNUM', 'A_ZSCORE']] = minmaxobj.inverse_transform(out[['CARDNUM', 'A_ZSCORE']])
out['CARDNUM']=out['CARDNUM'].round()

productidList=out['CARDNUM'].unique()
out['A_ZSCORE'].mode()
resultDict=dict()
for productid in productidList:
  temp=max(out['A_ZSCORE'][out['CARDNUM']==productid][out['outlier']==0])
  resultDict[productid]=temp
print(resultDict)

l= out.loc[out['outlier'] == 1].index.values.tolist()
outliers = df[df.index.isin(l)]

outliers.to_csv(output_base_path + "/" +outputFilename)