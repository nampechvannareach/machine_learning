import os 
import sys 
import numpy as np 
import pandas as pd 
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

#save obj
import os
import pickle
import sys
from src.exception import CustomException

def save_obj(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # remove file if exists (prevents permission issues)
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
#evalute obj 
def evalute_models(X_train, y_train, X_test, y_test, models, param):
    try:
        reports = {}

        for model_name, model in models.items():

            # ✅ correct param access
            para = param[model_name]

            # grid search
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            # best model
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # predictions
            y_test_pred = model.predict(X_test)

            # score
            test_model_score = r2_score(y_test, y_test_pred)

            # save result
            reports[model_name] = test_model_score

        return reports

    except Exception as e:
        raise CustomException(e, sys)

#load obj
def load_obj(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)