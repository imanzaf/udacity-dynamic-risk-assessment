'''
Read data files from source folder and write to master file
'''

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime


# Function for data ingestion
def merge_multiple_dataframe(input_folder_path,
                             output_folder_path,
                             output_file_name):
    # check for datasets and record
    filenames = os.listdir(os.getcwd() + '/' + input_folder_path + '/')

    # initialize empty df
    global compiled_df
    compiled_df = pd.DataFrame()

    # import and compile datasets
    if filenames:
        for file in filenames:
            data = pd.read_csv(os.path.join(os.getcwd(), input_folder_path, file))
            compiled_df = pd.concat([compiled_df, data], ignore_index=True)

    # drop duplicates and write to output path
    compiled_df.drop_duplicates(inplace=True)
    compiled_df.to_csv(os.path.join(os.getcwd(), output_folder_path, output_file_name))


# Function for recording ingestion
def record_ingestion(input_folder_path, output_folder_path):

    # get file names
    location = os.path.join(os.getcwd(), input_folder_path)
    filenames = os.listdir(os.getcwd() + '/' + input_folder_path + '/')
    time = str(datetime.now())
    record = {'location':location,
              'files': filenames,
              'time at ingestion':time}

    # write to txt file
    with open(os.path.join(output_folder_path, 'ingestedfiles.txt'), 'w') as f:
        f.write(json.dumps(record))


if __name__ == '__main__':
    # Load config file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Get input and output paths
    input_folder_path = config['input_folder_path']
    output_folder_path = config['output_folder_path']
    output_file_name = 'finaldata.csv'

    # Ingest data
    merge_multiple_dataframe(input_folder_path,
                             output_folder_path,
                             output_file_name)

    # Record ingestion
    record_ingestion(input_folder_path,
                     output_folder_path)
