import joblib
import pandas as pd
import argparse 
from azureml.core.model import Model
from utils import retrieve_workspace
import os

# from inference_schema.schema_decorators import input_schema, output_schema
# from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType

model = None

def init():
    global model

    # If you deploy the model in a custom docker
    # ws = retrieve_workspace()
    # model_name = 'model_name here'
    # model_reg = Model(ws, name = model_name)
    # model_reg.download('./model', exist_ok = False)
    # model = joblib.load('./model/model_name)
    # model_path = Model.get_model_path()


    # Retrieve the path to the model file using the model name
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), '<model name here>')

    model = joblib.load(model_path)


# if you want to show examples in swaager
# input_sample = np.array([[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]])
# output_sample = np.array([3726.995])

# @input_schema('data', NumpyParameterType(input_sample))
# @output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        result = model.predict(data)
        # You can return any data type, as long as it is JSON serializable.
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error