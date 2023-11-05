from flask import Flask,render_template,jsonify,request
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
#from dagshub import dagshub_logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
import json
import mlflow
import os
from fit_model import fit_model
from clean_data import clean_data
app = Flask(__name__)


os.environ['MLFLOW_TRACKING_USERNAME']= "kallel.medanis"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "4d6fd1f20698281fab0a86cd6f176e0458a6a720"


mlflow.set_tracking_uri('https://dagshub.com/kallel.medanis/CreditRiskMLOPS.mlflow')

#let's call the model from the model registry ( in production stage)


models = {
    "RandomForest": RandomForestClassifier(),
    "LogisticRegression": LogisticRegression(),
    "SVM": SVC(),
    "DecisionTree": DecisionTreeClassifier(),
    "GaussianNB": GaussianNB(),
    "KNeighbors": KNeighborsClassifier()
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        jsonData = request.get_json()
        message = {'greeting':'Hello from Flask!'}
        return jsonify(jsonData)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        jsonData = request.get_json()
        X_train,X_test,y_train,y_test = clean_data(jsonData)[0]
        mlflow.sklearn.autolog(disable=True)
        for model_name, model in models.items():
            fit_model(X_train,X_test,y_train,y_test,model_name,model)
        
        #let's call the model from the model registry ( in production stage)

        df_mlflow = mlflow.search_runs(filter_string="metrics.F1_score_test<1")
        run_id = df_mlflow.loc[df_mlflow['metrics.F1_score_test'].idxmax()]['run_id']

        logged_model = f'runs:/{run_id}/ML_models'

        model = mlflow.pyfunc.load_model(logged_model)
        
        res=model.predict(np.array(clean_data(jsonData)[1]).reshape(1, -1))[0]

        new_row=clean_data(jsonData)[2].update({"risk_flag":res})

        df=pd.read_csv('Df.csv')

        df=df.append(new_row, ignore_index=True)

        df.to_excel('Df.csv', index=False)

        return {"res":str(res)}

@app.route('/adasd')
def adsd():
    return render_template("index.html")


@app.route('/adssd')
def adssd():
    MS=request.args.get('MS')
    HO=request.args.get('HO')
    CO=request.args.get('CO')
    income=request.args.get('income')
    age=int(request.args.get('age'))
    experience=int(request.args.get('experience'))
    state=request.args.get('state')
    currYears=int(request.args.get('currYears'))
    df=pd.read_csv('Df.csv')

    leM = preprocessing.LabelEncoder()
    leHO = preprocessing.LabelEncoder()
    leCO = preprocessing.LabelEncoder()
    leS = preprocessing.LabelEncoder()
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
    DT=DecisionTreeClassifier()
    DT.fit(X, y)
    res=DT.predict(np.array([income,age,experience,marriedLE,house_ownershipLE,car_ownershipLE,stateLE,currYears]).reshape(1, -1))[0]
    return res



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
