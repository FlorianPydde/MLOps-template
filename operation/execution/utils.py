from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

import os
import sys
import json
from pathlib import Path

def retrieve_workspace() -> Workspace:
    ws = None

    try:
        ws = Workspace.from_config()
        return ws

    except Exception as e:
        print('Workspace not found in local repo.')
        print('Trying Service Principal')

    
    try:
        sp = ServicePrincipalAuthentication(
            tenant_id=os.environ['AML_TENANT_ID'],
            service_principal_id=os.environ['AML_PRINCIPAL_ID'],
            service_principal_password=os.environ['AML_PRINCIPAL_PASS']
            )

        ws = Workspace.get(
            name=os.environ['AML_WORKSPACE_NAME'],
            auth=sp,
            subscription_id=os.environ['SUBSCRIPTION_ID']
            )
        return ws
    except Exception as e:
        print('Connection via SP failed:', e)

    if not ws:
        print('Error - Workspace not found')
        print('Error - Shuting everything down.')
        sys.exit(-1)

# Retrieve config json
def retrieve_config():
    config = {}
    #go 2 layer up
    util_path = Path(__file__).parents[1]
    config_path = util_path / 'configuration' / 'configuration.json'
    with open(config_path, mode='r', encoding='utf-8') as input_file:
        config = json.load(input_file)
    return config
