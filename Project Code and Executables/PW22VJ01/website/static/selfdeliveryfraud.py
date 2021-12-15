import pandas as pd
import numpy as np
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier


print(os.getcwd())
curr_file_path = os.getcwd()
input_base_path = curr_file_path + "/uploads"

output_base_path = curr_file_path + "/downloads"  
os.chdir(input_base_path) 

inputFilename = os.listdir()[0]  
outputFilename = "selfdeliveryfrauds_1.csv"

print(inputFilename)

df = pd.read_csv(input_base_path + "/" + inputFilename)

df.USER_ID=pd.to_numeric(df.USER_ID,errors='coerce')
df.PRODUCT_ID=pd.to_numeric(df.PRODUCT_ID,errors='coerce')
df.RATING=pd.to_numeric(df.RATING,errors='coerce')
df.USER_ID.unique()

target_prod=33
target_acc=91

totrat=0
thisacc=0
takecounttot=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc)]
takeacc=df[df['PRODUCT_ID'] == target_prod]
intmed=df[df['PRODUCT_ID'] == target_prod]
intmed.USER_ID.unique()
tarprod=df[df['PRODUCT_ID'] == target_prod]
taracc=tarprod[(df['USER_ID'] == target_acc) & (pd.notnull(df['PRODUCT_ID'])) ]
tarpincodes=taracc.ZIPCODE.unique()
freqzip=0
totfreqcount=tarprod['ZIPCODE'].value_counts()
totalsumofpincodes=totfreqcount.sum()
for i in tarpincodes:
    freqzip+=totfreqcount[i]/totalsumofpincodes
tartrans=df[(df['PRODUCT_ID']== target_prod) & (df['USER_ID'] == target_acc)]
tottrans=df[(df['USER_ID'] == target_acc) & (pd.notnull(df['PRODUCT_ID']))]
totratings=len(df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc)])
star5rating=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc) & (df['RATING'] == 5)]
star4rating=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc) & (df['RATING'] == 4)]
star1rating=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc) & (df['RATING'] == 1)]
listofusers=df['USER_ID'].unique()
productidlist=df['PRODUCT_ID'].unique()
headers=["Accountname","Product_ID","% of total ratings by this account","of this account's pincode to that of total product's delivery pincode","% of the account's total transactions to this product"," % 5 star","% 4 star"," % 1 star"]
newdf=pd.DataFrame(columns=headers)

newdf=12
result=[]
for users in listofusers:
    for products in productidlist:
        if newdf!=None and pd.notnull(users) and pd.notnull(products):
            data=[]
            data.append(users)
            data.append(products)            
            target_prod=products
            target_acc=users
            if len(df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc)])==0:
                continue
            takecounttot=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc)]
            takeacc=df[df['PRODUCT_ID'] == target_prod]
            percenttotrating=len(takecounttot)/len(takeacc)*100
            data.append(percenttotrating)
            tarprod=df[df['PRODUCT_ID'] == target_prod]
            taracc=tarprod[(df['USER_ID'] == target_acc) & (pd.notnull(df['PRODUCT_ID'])) ]
            tarpincodes=taracc.ZIPCODE.unique()
            freqzip=0
            totfreqcount=tarprod['ZIPCODE'].value_counts()
            totalsumofpincodes=totfreqcount.sum()
            for i in tarpincodes:
                freqzip+=totfreqcount[i]/totalsumofpincodes
            percentpincode=freqzip*100
            data.append(percentpincode)
            tartrans=df[(df['PRODUCT_ID']== target_prod) & (df['USER_ID'] == target_acc)]
            tottrans=df[(df['USER_ID'] == target_acc) & (pd.notnull(df['PRODUCT_ID']))]
            percenttrans=len(tartrans)/len(tottrans)*100
            data.append(percenttrans)
            totrating=len(df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc)])
            star5rating=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc) & (df['RATING'] == 5)]
            star4rating=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc) & (df['RATING'] == 4)]
            star1rating=df[(df['PRODUCT_ID'] == target_prod) & (df['USER_ID'] == target_acc) & (df['RATING'] == 1)]
            percent5star=len(star5rating)/totrating*100
            data.append(percent5star)
            percent4star=len(star4rating)/totrating*100
            data.append(percent4star)
            percent1star=len(star1rating)/totrating*100
            data.append(percent1star)
            result.append(data)
        else:
            pass
            
newdf=pd.DataFrame(result,columns=headers)

# print("Currently here : " +os.getcwd())
os.chdir(curr_file_path)
loaded_rf = joblib.load("random_forest.joblib")
labels=loaded_rf.predict(newdf)
newdf['Output']=labels
fraud = newdf[newdf['Output']=="fraud"]
fraud.to_csv(output_base_path + "/" + outputFilename)