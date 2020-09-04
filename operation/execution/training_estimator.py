from azureml.core import Experiment
from azureml.core.environment import Environment
from azureml.core.compute import ComputeTargetException,ComputeTarget
from azureml.train.estimator import Estimator
from azureml.train.dnn import TensorFlow
from azureml.core.dataset import Dataset

import os
import sys
import utils
from pathlib import Path

#retrieve workspace
#get experiment name
ws =  utils.retrieve_workspace()
if ws is None:
    sys.exit(-1)

experiment = Experiment(workspace=ws, name='myexp')


try:
    compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", "cpucluster")
    compute_target = ws.compute_targets[compute_name]
except Exception as e:
    print('Error while retrieving compute', e)
    sys.exit(-1)

env = None
try:
    env = Environment.get(workspace=ws, name=os.environ.get('AML_ENVIRONMENT','myenv'))
except Exception as e:
    print('Environment not found in workspace')
    print('Trying to retrieve from local config')

if env is None:
    try:
        dir_path = Path(__file__).resolve().parent.parent
        env_path = dir_path / '< folder to use >'
        env = Environment.load_from_directory(path = env_path)
    except Exception as e:
        print('Environment folder not found')
        print('Shutting everything down !')
        sys.exit(-1)

#####################
#If you are using datasets
#dataset = Dataset.get_by_name(ws, 'mnist-dataset')
#####################

# Some script parameters
script_params = {
    'some_script_param':''
    # to mount files referenced by mnist dataset
    # '--data-folder': mnist_file_dataset.as_named_input('mnist_opendataset').as_mount(),
    # '--regularization': 0.5
}

# Simple estimator
est = Estimator(
    source_directory='./src',
    entry_script='train.py',
    script_params=script_params,
    compute_target=compute_target,
    environment_definition=env,
    )

# More advanced estimator
est = TensorFlow(source_directory='./src',
                 entry_script='train.py',
                 compute_target=compute_target, 
                 script_params=script_params,
                 framework_version='2.0', 
                 # if you need more specific packages
                 pip_packages=['keras<=2.3.1','azureml-dataset-runtime[pandas,fuse]','matplotlib'])

run = experiment.submit(config=est)

