import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams["figure.figsize"]=(20,10)
###DATA CLEANING AND REMOVE UNNECSSARY INFORMATION
#most unfiltered data frame
df1 = pd.read_csv("D:\RealEstatePricePrediction\Dehli_House_Data.csv")
df1.head()
df1.shape
#drop some columns which is not importent and creat new data frame df2
df2 = df1.drop(["Transaction","Status",'Per_Sqft'],axis='columns')
df2.head()
df2.shape
#find total null value in data frame
df2.isnull().sum()
#drop those data which is store null value and creat new data frame df3
df3 = df2.dropna()
df3.isnull().sum()
#find uniq data in columns
df3['Area'].unique()
#creating new data frame which has new column called 'price per sqft'
df4 = df3.copy()
df4['Price_per_sqft']=df4['Price']/df4['Area']
df4.head()
###REMOVAL OUTLIER
#every location is come how many time
len(df4.Locality.unique())
df4.Locality=df4.Locality.apply(lambda x:x.strip())
Locality_stats = df4.groupby('Locality')['Locality'].agg('count').sort_values(ascending=False)
Locality_stats
#how many location use less the 10
len(Locality_stats[Locality_stats<=10])
Locality_stats_less_then_10 = Locality_stats[Locality_stats<=10]
Locality_stats_less_then_10
len(df4.Locality.unique())
#if Locality stats are less the 10 add in other Locality
df4.Locality = df4.Locality.apply(lambda x: 'other' if x in Locality_stats_less_then_10 else x)
len(df4.Locality.unique())
df4.head(30).Locality

#remove outliers on bhk in sqft
df4[df4.Area/df4.BHK<250].head()
df5= df4[~(df4.Area/df4.BHK<250)]
df5.shape
df5.Price_per_sqft.describe()
#remove price pre sqft outliers
def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('Locality'):
        m = np.mean(subdf.Price_per_sqft)
        st = np.std(subdf.Price_per_sqft)
        reduced_df = subdf[(subdf.Price_per_sqft>(m-st)) & (subdf.Price_per_sqft)]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out
df6=remove_pps_outliers(df5)
df6.shape
df6.head()
#create histogram price per square feet and number of proportice
matplotlib.rcParams["figure.figsize"]=(20,10)
plt.hist(df6.Price_per_sqft,rwidth=0.8)
plt.xlabel("Price per Square Feet")
plt.ylabel("Count")

df6.Bathroom.unique()

####MODEL BUILDING
df7 =df6.drop(['Price_per_sqft'],axis='columns')
df7.head(30)
#conver Locality name in binary form using hot coding & dummies
dummies = pd.get_dummies(df7.Locality)
dummies.head(10)
df8 = pd.concat([df7,dummies.drop('other',axis='columns')], axis='columns')
df8.head(3)
#conver Furnishing in binary form using hot coding & dummies
dummies1 = pd.get_dummies(df8.Furnishing)
df9 = pd.concat([df8,dummies1],axis='columns')
df9.head()
#conver Type in binary
dummies2 = pd.get_dummies(df9.Type)
df10 = pd.concat([df9,dummies2],axis='columns')
df10.head()
#remove Locality Furnishing Type
df11 = df10.drop(['Locality','Furnishing','Type'],axis='columns')
df11.head(10)
#differentiate dependent variable and independent variable like price and another
independent=df11.drop('Price',axis='columns')
independent.head()
dependent = df11.Price
dependent.head()
#train test split method
from sklearn.model_selection import train_test_split
independent_train,independent_test,dependent_train,dependent_test=train_test_split(independent,dependent,test_size=0.2,random_state=10)
#Linear Regression model
from sklearn.linear_model import LinearRegression
lr_cif = LinearRegression()
lr_cif.fit(independent_train,dependent_train)
lr_cif.score(independent_test,dependent_test)


#shuffle split for cross-validation
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score

cv = ShuffleSplit(n_splits=5,test_size=0.2,random_state=0)
cross_val_score(LinearRegression(),independent,dependent,cv=cv)

#predict price
independent.columns
def predict_price(Locality, Furnishing, Type, Area, BHK, Bathroom, Parking):
    loc_index = np.where(independent.columns == Locality)[0][0]
    fur_index = np.where(independent.columns == Furnishing)[0][0]
    type_index = np.where(independent.columns == Type)[0][0]
    
    independent_input = np.zeros(len(independent.columns))
    independent_input[0] = Area
    independent_input[1] = BHK
    independent_input[2] = Bathroom
    independent_input[3] = Parking
    
    if loc_index >= 0:
        independent_input[loc_index] = 1
    if fur_index >= 0:
        independent_input[fur_index] = 1
    if type_index >= 0:
        independent_input[type_index] = 1
    
    return lr_cif.predict([independent_input])[0]

print("Locality are : ",df7["Locality"].unique())
print("Furnishing are : ",df7["Furnishing"].unique())
print("Types are : ",df7["Type"].unique())

predicted_price = predict_price('Alaknanda', 'Furnished', 'Apartment', 1500, 3, 3, 1)
print("Price is : ",predicted_price)
import pickle
import json
#saving model
with open("Dehli_House_Data_Model.pickle",'wb') as f:
    pickle.dump(lr_cif, f)
#save columns name
columns = {
    'data_columns':[col.lower() for col in independent.columns]
    }
with open("dehli_data_columns.json","w")as f:
    json.dump(columns,f)