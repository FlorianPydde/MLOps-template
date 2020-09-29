from azureml.core import Run, Dataset, Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.run import _OfflineRun
import argparse
import sys
import os
from pathlib import Path
import pandas as pd

def retrieve_workspace() -> Workspace:
    ws = None

    try:
        run = Run.get_context()
        if not isinstance(run,_OfflineRun):
            ws = run.experiment.workspace
            return ws
    except Exception as e:
        print('Workspace from run not found', e)

    try:
        ws = Workspace.from_config()
        return ws
    except Exception as e:
        print('Workspace config not found in local folder', e)

    try:
        sp = ServicePrincipalAuthentication(tenant_id=os.environ['AML_TENANT_ID'],
                                    service_principal_id=os.environ['AML_PRINCIPAL_ID'],
                                    service_principal_password=os.environ['AML_PRINCIPAL_PASS']
                                    )
        ws = Workspace.get(name="ml-example",
                   auth=sp,
                   subscription_id="your-sub-id")
    except Exception as e:
        print('Workspace config not found in project', e)
    
    return ws

def get_dataset(filename:str = '', datastore:str = '', path_datastore:str = ''):

    df = None
    #get the data when run by external scripts

    try:
        run = Run.get_context()
        if not isinstance(run,_OfflineRun):
            dataset = run.input_datasets[filename]
            df = dataset.to_pandas_dataframe()
            return df
    except Exception as e:
        print('Dataset not present in run', e)
    
    #get dataset from datastore/Dataset registry
    try:
        ws = retrieve_workspace()
        datastore = ws.get_default_datastore()
        dataset = Dataset.File.from_files(path = [(datastore,path_datastore)])
        df = dataset.to_pandas_dataframe()
    except Exception as e:
        print('Error while retrieving from datastore',e)

    #load from pandas
    #df = pd.from_csv()
    if df is None:
        print('Launch error here')
        sys.exit(-1)

    return df