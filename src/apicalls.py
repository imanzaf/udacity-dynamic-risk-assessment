import requests
import json
import os

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000/"

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f)

test_data_path = os.path.join(config['test_data_path'])
output_path = os.path.join(config['output_model_path'])


#Call each API endpoint and store the responses
# call prediction endpoint
file_location = os.path.join(os.getcwd(), test_data_path, 'testdata.csv')
pred_resp = requests.post(f'{URL}/prediction?filelocation={file_location}').text

# call scoring endpoint
score_resp = requests.get(f'{URL}/scoring').text

# call summary stats endpoint
stats_resp = requests.get(f'{URL}/summarystats').text

# call diagnostics endpoint
diag_resp = requests.get(f'{URL}/diagnostics').text


#combine all API responses
#write the responses to your workspace
with open(os.path.join(os.getcwd(), output_path, 'apireturns.txt'), 'w') as f:
    f.write(f'Predictions: {pred_resp}\n')
    f.write(f'Model Score: {score_resp}\n')
    f.write(f'Summary Statistics:\n {stats_resp}\n')
    f.write(f'Model Diagnostics: \n {diag_resp}\n')
