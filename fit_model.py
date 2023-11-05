import pandas as pd
import pickle
import datetime as dt
import mlflow
from sklearn.metrics import precision_recall_fscore_support as score

def fit_model(X_train,X_test,y_train,y_test,model_name,model):
    with mlflow.start_run(run_name=model_name):
        #mlflow.log_param("data_url",data_url)
        #mlflow.log_param("data_version",version)
        #mlflow.log_param("input_rows",df.shape[0])
        #mlflow.log_param("input_cols",df.shape[1])
        #model fitting and training
        lr=model
        mlflow.set_tag(key= "model",value=model_name)
        params = lr.get_params()
        mlflow.log_params(params)
        lr.fit(X_train,y_train)
        train_features_name = f'{X_train=}'.split('=')[0]
        train_label_name = f'{y_train=}'.split('=')[0]
        mlflow.set_tag(key="train_features_name",value= train_features_name)
        mlflow.set_tag(key= "train_label_name",value=train_label_name)
        predicted=lr.predict(X_test)
        precision,recall,fscore,support=score(y_test,predicted,average='macro')
        mlflow.log_metric("Precision_test",precision)
        mlflow.log_metric("Recall_test",recall)
        mlflow.log_metric("F1_score_test",fscore)
        mlflow.sklearn.log_model(lr,artifact_path="ML_models")