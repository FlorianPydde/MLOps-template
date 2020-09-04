from azureml.core import Workspace, Environment
from pathlib import Path
import json

ws = Workspace.from_config()

list_env = Environment.list(workspace=ws)

def show_available_environment():
    for env in list_env:
        if env.startswith("AzureML"):
            print("Name",env)
            print("packages", list_env[env].python.conda_dependencies.serialize_to_string())


print(Path(__file__).parent)
with open(Path(__file__).parent / 'configuration.json', 'r') as config_file:
    config = json.load(config_file)

name = config['environment_name']
env = Environment.get(workspace=ws, name=name)

# From a Conda specification file
# myenv = Environment.from_conda_specification(name = "myenv",file_path = "path-to-conda-specification-file")

# From a pip requirements file
# myenv = Environment.from_pip_requirements(name = "myenv", file_path = "path-to-pip-requirements-file") 

#From an existing Conda environment
# myenv = Environment.from_existing_conda_environment(name = "myenv",conda_environment_name = "mycondaenv") 

#From exisitng yml file
# myenv = Environment.load_from_directory(path = "path-to-source-directory")

#

Environment.save_to_directory(env, path = Path("./operation/configuration/environment_dev"), overwrite = True)
Environment.save_to_directory(env, path = Path("./operation/configuration/environment_stage"), overwrite = True)
Environment.save_to_directory(env, path = Path("./operation/configuration/environment_prod"), overwrite = True)
