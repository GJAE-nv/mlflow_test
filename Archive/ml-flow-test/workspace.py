from azureml.core import Workspace

def get_workspace():

    ws = Workspace.get(name='ml-flow-test', subscription_id='b242efdc-f14b-4f3e-a454-0377fa50302b', resource_group='MLflow-analytics')
    return ws

if __name__ == '__main__':
    workspace = get_workspace()
    print("ok")