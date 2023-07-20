from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import json


# Function for model scoring
def score_model(model, data, features, target, output_path):
    # Subset X and y
    X = data[features]
    y = data[target]

    # Generate predictions
    preds = model.predict(X)

    # Calculate F1 score
    score = f1_score(y, preds)
    print(score)

    # write to file
    with open(os.getcwd()+'/'+output_path+'/latestscore.txt', 'w') as f:
        f.write(str(score))


if __name__ == '__main__':
    # Load config.json and get path variables
    with open('config.json', 'r') as f:
        config = json.load(f)

    model_path = os.path.join(config['output_model_path'])
    test_data_path = os.path.join(config['test_data_path'])

    # load model and data
    model = pickle.load(open(os.getcwd()+'/'+model_path+'/trainedmodel.pkl', 'rb'))
    df = pd.read_csv(os.getcwd()+'/'+test_data_path+'/testdata.csv')

    # score model
    features = ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
    target = 'exited'
    score_model(model, df, features, target, model_path)
