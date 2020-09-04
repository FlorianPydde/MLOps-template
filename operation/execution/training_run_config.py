from azureml.core import Experiment
from azureml.core.environment import Environment
from azureml.core.compute import ComputeTarget, ComputeTargetException
from azureml.core import ScriptRunConfig

import os
import sys
import utils
from pathlib import Path
#retrieve workspace
#get experiment name
ws =  utils.retrieve_workspace()
experiment = Experiment(workspace=ws, name='myexp')

#get compute target
try:
    compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", "cpucluster")
    compute_target = ws.compute_targets[compute_name]
except ComputeTargetException as e:
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


src = ScriptRunConfig(source_directory='./src', script='/train.py')
# Set compute target to the one created in previous step
src.run_config.target = compute_target.name
# Set environment
src.run_config.environment = env
run = experiment.submit(config=src)

# ----------------------------------------------------------

###########################
#Training with HDInsight
###########################

# ----------------------------------------------------------

from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.compute import ComputeTarget, HDInsightCompute
from azureml.exceptions import ComputeTargetException
import os

try:
    attach_config = HDInsightCompute.attach_configuration(resource_id='<resource_id>',
                                                          ssh_port=22,
                                                          username=os.environ.get('hdiusername', '<ssh_username>'),
                                                          password=os.environ.get('hdipassword', '<my_password>'))

    hdi_compute = ComputeTarget.attach(workspace=ws, 
                                       name='myhdi', 
                                       attach_configuration=attach_config)

except ComputeTargetException as e:
    print("Caught = {}".format(e.message))
    
        
hdi_compute.wait_for_completion(show_output=True)

# use pyspark framework
hdi_run_config = RunConfiguration(framework="pyspark")

# Set compute target to the HDI cluster
hdi_run_config.target = hdi_compute.name

# specify CondaDependencies object to ask system installing numpy
cd = CondaDependencies(env_path / 'conda_dependencies.yml')
hdi_run_config.environment.python.conda_dependencies = cd

script_run_config = ScriptRunConfig(source_directory = '.',
                                    script= 'train-spark.py',
                                    run_config = hdi_run_config)
                                    
run = experiment.submit(config=script_run_config)