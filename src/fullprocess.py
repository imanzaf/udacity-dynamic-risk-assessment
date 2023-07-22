
import os
import json
import pickle
import pandas as pd
import training
import scoring
import deployment
import diagnostics
import reporting
import subprocess


def main():

    print('Checking for new data...')
    # Checking for new data
    # read ingestedfiles.txt
    with open(os.path.join(os.getcwd(), config['prod_deployment_path'], 'ingestedfiles.txt'), 'r') as f:
        ingested = json.loads(f.read())['files']

    # check for new files
    files = os.listdir(os.path.join(os.getcwd(), config['input_folder_path']))
    new_data = [f for f in files if f not in ingested]

    if len(new_data) != 0:
        subprocess.run(['python', 'src/ingestion.py'])
    else:
        print("No new data found")
        exit()


    print('Checking for model drift...')
    # Checking for model drift
    # Import latest score, model, and new data
    with open(os.path.join(os.getcwd(), config['prod_deployment_path'], 'latestscore.txt'), 'r') as f:
        score = f.read()
    model = pickle.load(open(os.path.join(os.getcwd(), config['prod_deployment_path'], 'trainedmodel.pkl'), 'rb'))
    data = pd.read_csv(os.path.join(os.getcwd(), config['output_folder_path'], 'finaldata.csv'))

    # calculate new score
    new_score = scoring.score_model(model, data,
                                    ['lastmonth_activity', 'lastyear_activity', 'number_of_employees'], 'exited')

    # Deciding whether to proceed
    if float(new_score) >= float(score):
        print(float(new_score), '>=', float(score))
        print("Model drift not found")
        exit()


    # Re-deployment
    print("Training and deploying new model...")
    subprocess.run(['python', 'src/training.py'])
    subprocess.run(['python', 'src/scoring.py'])
    subprocess.run(['python', 'src/deployment.py'])

    # Diagnostics and reporting
    print("Running model diagnostics...")
    subprocess.run(['python', 'src/reporting.py'])
    subprocess.run(['python', 'src/apicalls.py'])


if __name__ == '__main__':

    # Load config.json and get path variables
    with open('config.json', 'r') as f:
        config = json.load(f)

    main()
