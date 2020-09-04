import logging
import sys
import os
import utils
from azureml.train.automl import AutoMLConfig
from azureml.core.compute import ComputeTargetException,ComputeTarget


ws =  utils.retrieve_workspace()
if ws is None:
    sys.exit(-1)

try:
    compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", "cpucluster")
    compute_target = ws.compute_targets[compute_name]
except Exception as e:
    print('Error while retrieving compute', e)
    sys.exit(-1)

automl_settings = {
    "iteration_timeout_minutes": 2,
    "experiment_timeout_hours": 0.3,
    "enable_early_stopping": True,
    "primary_metric": 'spearman_correlation',
    "featurization": 'auto',
    "verbosity": logging.INFO,
    "n_cross_validations": 5
}

automl_config = AutoMLConfig(task='regression',
                             debug_log='automated_ml_errors.log',
                             compute_target = compute_target,
                             training_data='provide training data here',
                             label_column_name="totalAmount",
                             **automl_settings)
