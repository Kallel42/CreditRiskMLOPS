import pandas as pd
import pickle
import datetime as dt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
def clean_data(jsonData):
    MS=jsonData["MS"]
    MS=jsonData["MS"]
    HO="rented"
    CO=jsonData["CO"]
    income=jsonData["income"]
    age=jsonData["age"]
    experience=jsonData["experience"]
    state=jsonData["state"]
    currYears=jsonData["currYears"]
    leM = preprocessing.LabelEncoder()
    leHO = preprocessing.LabelEncoder()
    leCO = preprocessing.LabelEncoder()
    leS = preprocessing.LabelEncoder()
    df=pd.read_csv('Df.csv')
    df["married"]=leM.fit_transform(df["married"])
    df["house_ownership"]=leHO.fit_transform(df["house_ownership"])
    df["car_ownership"]=leCO.fit_transform(df["car_ownership"])
    df["state"]=leS.fit_transform(df["state"])
    marriedLE=leM.transform([MS])[0]
    house_ownershipLE=leHO.transform([HO])[0]
    car_ownershipLE=leCO.transform([CO])[0]
    stateLE=leS.transform([state])[0]
    X=df.drop("risk_flag",axis=1)
    y=df["risk_flag"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    return ((X_train,X_test,y_train,y_test),(income,age,experience,marriedLE,house_ownershipLE,car_ownershipLE,stateLE,currYears),({"income":income,"age":age,"experience":experience,"married":MS,"house_ownership":HO,"car_ownership":CO,"state":state,"current_job_years":currYears}))