import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions


# Function for reporting
def score_model(model, test_data, features, label, output_path):

    #calculate a confusion matrix using the test data and the deployed model
    preds = model_predictions(model, test_data, features)
    y_true = test_data[label]

    scores = ConfusionMatrixDisplay(confusion_matrix(y_true, preds))

    # write to workspace
    scores.plot()
    scores.figure_.savefig(output_path)


if __name__ == '__main__':
    # Load config.json and get path variables
    with open('config.json', 'r') as f:
        config = json.load(f)

    model_path = os.path.join(config['output_model_path'])
    output_path = os.path.join(config['output_model_path'])
    test_data_path = os.path.join(config['test_data_path'])

    # Import model and data
    model = pickle.load(open(os.getcwd() + '/' + model_path + '/trainedmodel.pkl', 'rb'))
    df = pd.read_csv(os.getcwd() + '/' + test_data_path + '/testdata.csv')

    # define features and label
    features = ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
    label = 'exited'

    score_model(model, df, features, label,
                (os.getcwd() + '/' + output_path + '/confusionmatrix.png'))
