import joblib
import pandas as pd
from azureml.core.model import Model
# from inference_schema.schema_decorators import input_schema, output_schema
# from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType

def init():
    global model

    # Retrieve the path to the model file using the model name
    # Assume original model is named original_prediction_model
    
    model_path = Model.get_model_path('name of model',version=0)
    model = joblib.load(model_path)


#if you want to show examples in swaager
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