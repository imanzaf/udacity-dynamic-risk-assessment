from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json


# Function for training the model
def train_model(data, features, target):
    
    # Create Logistic Regression model
    model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='multinomial', n_jobs=None, penalty='l2',
                    random_state=0, solver='newton-cg', tol=0.0001, verbose=0,
                    warm_start=False)
    
    # Get X and y from data
    X = data[features]
    y = data[target]

    # Fit the logistic regression to data
    model.fit(X, y)

    # Write the trained model to file
    pickle.dump(model, open(os.path.join(os.getcwd(), model_path, 'trainedmodel.pkl'), 'wb'))


if __name__ == '__main__':
    # Load config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Get path variables
    dataset_csv_path = os.path.join(config['output_folder_path'])
    model_path = os.path.join(config['output_model_path'])

    # Import data
    df = pd.read_csv(os.path.join(os.getcwd(), dataset_csv_path, 'finaldata.csv'))

    # Train model
    features = ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
    target = 'exited'
    train_model(df, features, target)
