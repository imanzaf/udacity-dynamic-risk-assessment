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
            data = pd.read_csv(os.getcwd() + '/' + input_folder_path + '/' + file)
            compiled_df = compiled_df.append(data).reset_index(drop=True)
    # drop duplicates and write to output path
    compiled_df.drop_duplicates(inplace=True)
    compiled_df.to_csv(os.getcwd() + '/' + output_folder_path + '/' + output_file_name)
    return compiled_df


# Function for recording ingestion
def record_ingestion(output_folder_path, output_file_name, df):
    # get records
    location = os.getcwd() + '/' + output_folder_path + '/'
    time = str(datetime.now())
    record = {'location':location,
              'file name': output_file_name,
              'data length':len(df.index),
              'time at ingestion':time}

    # write to txt file
    with open(output_folder_path+'/'+'ingestedfiles.txt', 'w') as f:
        for key in record:
            f.write(key+': '+str(record[key])+'\n')


if __name__ == '__main__':
    # Load config file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Get input and output paths
    input_folder_path = config['input_folder_path']
    output_folder_path = config['output_folder_path']
    output_file_name = 'compiled_data.csv'

    # Ingest data
    compiled_df = merge_multiple_dataframe(input_folder_path,
                                           output_folder_path,
                                           output_file_name)

    # Record ingestion
    record_ingestion(output_folder_path,
                     output_file_name,
                     compiled_df)
