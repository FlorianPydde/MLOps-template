from azureml.core import Run, Dataset, Workspace
import argparse
import sys
from pathlib import Path
import pandas as pd
# get the input dataset by name

# load the TabularDataset to pandas DataFrame


def get_dataset(filename=str):

    df = None
    #get the data when run by external scripts

    # try:
    #     run = Run.get_context()
    #     #if you need some secrets:
    #     #secrets = run.get_secrets()
    #     dataset = run.input_datasets[filename]
    #     df = dataset.to_pandas_dataframe()

    # except Exception as e:
    #     print(e)
    
    #get dataset from datastore/Dataset registry
    # try:
    #     ws = Workspace.from_config(Path('./config.json'))
    #     datastore = ws.get_default_datastore()
    #     dataset = Dataset.File.from_files(path = [(datastore,'<path on datastore>')])
    #     df = dataset.to_pandas_dataframe()
    # except Exception as e:
    #     print(e)

    
    #load from pandas
    #df = pd.from_csv()
    if df is None:
        print('Launch error here')
        sys.exit(-1)

def train():
    #do your training here
    return 

if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--input_ds',default='./data', type=str, help='')
    args.add_argument('--output_dir',default='./output', type=str, help='')
    args.add_argument('--output_filename', default='model.pkl', type=str, help='')

    get_dataset()
