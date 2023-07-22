# Dynamic Risk Assessment System
This repository holds the fourth project completed towards Udacity's Machine Learning DevOps Engineer Nanodegree



### Project Overview
1. **Data ingestion**: Automatically check a database for new data that can be used for model training. Compile all training data to a training dataset and save it to persistent storage. Write metrics related to the completed data ingestion tasks to persistent storage.
2. **Training, scoring, and deploying**: Write scripts that train an ML model that predicts attrition risk, and score the model. Write the model and the scoring metrics to persistent storage.
3. **Diagnostics**: Determine and save summary statistics related to a dataset. Time the performance of model training and scoring scripts. Check for dependency changes and package updates.
4. **Reporting**: Automatically generate plots and documents that report on model metrics. Provide an API endpoint that can return model predictions and metrics.
5. **Process Automation**: Create a script and cron job that automatically run all previous steps at regular intervals.



### Running the files
The project can be run by running the fullprocess.py file using the below commands in the project's root directory

`pip install -r requirements.txt  # to install all requirements in the environment`

`python src/app.py  # To start the app`

`python src/fullprocess.py  # To run all steps at once`
