from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
# import create_prediction_model
# import diagnosis
# import predict_exited_from_saved_model
import json
import os
import subprocess
import re
from diagnostics import model_predictions, dataframe_summary, missing_data, execution_time, outdated_packages_list



# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json','r') as f:
    config = json.load(f) 

model_path = os.path.join(config['output_model_path'])
data_output_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])

prediction_model = None


@app.route("/")
def hello():
    greeting = 'Welcome to my app!'
    return greeting


# Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():
    # Get data
    file_location = request.args.get('filelocation')
    df = pd.read_csv(file_location)

    # Import model
    model = pickle.load(open(os.getcwd() + '/' + model_path + '/trainedmodel.pkl', 'rb'))

    # call prediction function
    preds = model_predictions(model, df,
                              ['lastmonth_activity', 'lastyear_activity', 'number_of_employees'])

    return preds.tolist()


# Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def score():
    # run scoring script
    scoring = subprocess.run(['python', 'src/scoring.py'], capture_output=True).stdout
    score = scoring.decode().replace(re.findall(r'[^(\d+\.\d+)]', scoring.decode())[0], '')
    return score


# Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats():        
    # get summary stats
    df = pd.read_csv(os.getcwd() + '/' + test_data_path + '/testdata.csv')
    summary = dataframe_summary(df)
    return summary.to_dict()


# Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def diagnostics():
    #check timing and percent NA values
    diagnostics_dict = {}
    df = pd.read_csv(os.getcwd() + '/' + test_data_path + '/testdata.csv')
    nulls = missing_data(df)
    diagnostics_dict['% of nulls'] = nulls
    time = execution_time()
    diagnostics_dict['execution time'] = time
    outdated = outdated_packages_list().split('\n')
    diagnostics_dict['outdated packages'] = outdated
    return diagnostics_dict


if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
