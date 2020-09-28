from azureml.core import Run, Dataset, Workspace
import argparse
import sys
from pathlib import Path
import pandas as pd
from utils import get_dataset
# get the input dataset by name

# load the TabularDataset to pandas DataFrame

def train():
    #do your training here
    return 

if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--input_ds',default='./data', type=str, help='')
    args.add_argument('--output_dir',default='./output', type=str, help='')
    args.add_argument('--output_filename', default='model.pkl', type=str, help='')

    #add filename, datastore or path on datastore depending on approach
    get_dataset(args.input_ds)
    train()
