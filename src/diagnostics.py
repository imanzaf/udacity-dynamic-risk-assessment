
import pandas as pd
import numpy as np
import timeit
import os
import json
import subprocess
import pickle


# Function to get model predictions
def model_predictions(model, data, features):

    # Get input data
    X = data[features]
    # Get predictions
    preds = model.predict(X)

    return preds


# Function to get summary statistics
def dataframe_summary(data):

    # Get numeric columns
    df = data.select_dtypes(include=np.number)
    # Get summary stats
    summary = df.describe()

    return summary


# Function to check for missing data
def missing_data(data):

    # Get numeric columns
    df = data.select_dtypes(include=np.number)
    # Get list of NA percentages
    NAs = ((df.isna().sum()/len(df.index))*100).to_list()

    return NAs


# Function to get timings
def execution_time():

    # Timing of training.py
    start_training = timeit.default_timer()
    os.system('python training.py')
    training_timing = timeit.default_timer() - start_training

    # Timing of ingestion.py
    start_ingestion = timeit.default_timer()
    os.system('python ingestion.py')
    ingestion_timing = timeit.default_timer() - start_ingestion

    return [training_timing, ingestion_timing]


# Function to check dependencies
def outdated_packages_list():
    #get a list of
    outdated = subprocess.check_output(['pip', 'list',
                                        '--outdated',
                                        'requirements.txt'], text=True)
    return outdated


if __name__ == '__main__':
    # Load config.json and get path variables
    with open('config.json', 'r') as f:
        config = json.load(f)

    model_path = os.path.join(config['output_model_path'])
    data_output_path = os.path.join(config['output_folder_path'])
    test_data_path = os.path.join(config['test_data_path'])

    # Import model and data
    model = pickle.load(open(os.getcwd() + '/' + model_path + '/trainedmodel.pkl', 'rb'))
    df = pd.read_csv(os.getcwd() + '/' + test_data_path + '/testdata.csv')

    # Run functions
    preds = model_predictions(model, df,
                              ['lastmonth_activity', 'lastyear_activity', 'number_of_employees'])
    print('No. of predictions: ', len(preds))

    summary = dataframe_summary(df)
    print('Data summary:\n', summary)

    nulls = missing_data(df)
    print('% of nulls: ', nulls)

    print('Execution times: ', execution_time())

    print('Outdated packages:\n')
    outdated = outdated_packages_list().split('\n')
    for item in outdated:
        print(item, '\n')
