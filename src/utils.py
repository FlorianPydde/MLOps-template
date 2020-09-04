from azureml.core import Run, Dataset, Workspace
import argparse
import sys
from pathlib import Path
import pandas as pd

def retrieve_workspace() -> Workspace:
    ws = None

    try:
        run = Run.get_context()
        ws = run.experiment.workspace
    except Exception as e:
        print('Workspace from run not found', e)

    try:
        ws = Workspace.from_config()
    except Exception as e:
        print('Workspace config not found in project', e)
    
    return ws

def get_dataset(filename=str):

    df = None
    #get the data when run by external scripts

    try:
        run = Run.get_context()
        dataset = run.input_datasets[filename]
        df = dataset.to_pandas_dataframe()
    except Exception as e:
        print('Dataset not present in run', e)
    
    #get dataset from datastore/Dataset registry
    try:
        ws = retrieve_workspace()
        datastore = ws.get_default_datastore()
        dataset = Dataset.File.from_files(path = [(datastore,'<path on datastore>')])
        df = dataset.to_pandas_dataframe()
    except Exception as e:
        print('Error while retrieving from datastore',e)

    #load from pandas
    #df = pd.from_csv()
    if df is None:
        print('Launch error here')
        sys.exit(-1)

    return df