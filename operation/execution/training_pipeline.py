from azureml.core import Experiment
from azureml.core.environment import Environment
from azureml.core.compute import ComputeTarget, ComputeTargetException
from azureml.pipeline.steps import ParallelRunConfig, ParallelRunStep, EstimatorStep
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.core.dataset import Dataset

from datetime import datetime
import sys
from pathlib import Path
import os
import utils

ws =  utils.retrieve_workspace()
experiment = Experiment(workspace=ws, name='myexp')
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

#get compute target
try:
    compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", "cpucluster")
    compute_target = ws.compute_targets[compute_name]
except ComputeTargetException as e:
    print('Error while retrieving compute', e)
    sys.exit(-1)


################################
# If you want to use datastore
################################
# from azureml.core import Datastore
# from azureml.data.data_reference import DataReference
# from azureml.pipeline.core import PipelineData

# def_blob_store = Datastore(ws, "workspaceblobstore")

# input_data = DataReference(
#     datastore=def_blob_store,
#     data_reference_name="input_data",
#     path_on_datastore="20newsgroups/20news.pkl")

# output = PipelineData("output", datastore=def_blob_store)


est_step = EstimatorStep(name="Estimator_Train", 
                         estimator=est, 
                         estimator_entry_script_arguments=["--datadir", input_data, "--output", output],
                         runconfig_pipeline_params=None, 
                         inputs=[input_data], 
                         outputs=[output], 
                         compute_target=compute_target)

pipeline = Pipeline(workspace=ws, steps=[est_step])
pipeline_run = experiment.submit(pipeline)