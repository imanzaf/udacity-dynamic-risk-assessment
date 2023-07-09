from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json
import shutil


# function for deployment
def deploy_model(model_source, data_source, destination):
    # copy model
    shutil.copyfile(os.getcwd() + '/' + model_source + '/trainedmodel.pkl',
                    os.getcwd() + '/' + destination + '/trainedmodel.pkl')

    # copy model score
    shutil.copyfile(os.getcwd() + '/' + model_source + '/latestscore.txt',
                    os.getcwd() + '/' + destination + '/latestscore.txt')

    # copy data record
    shutil.copyfile(os.getcwd() + '/' + data_source + '/ingestedfiles.txt',
                    os.getcwd() + '/' + destination + '/ingestedfiles.txt')
        
        
if __name__ == '__main__':
    # Load config.json and correct path variable
    with open('config.json', 'r') as f:
        config = json.load(f)

    model_path = os.path.join(config['output_model_path'])
    dataset_csv_path = os.path.join(config['output_folder_path'])
    prod_deployment_path = os.path.join(config['prod_deployment_path'])

    deploy_model(model_path, dataset_csv_path, prod_deployment_path)
