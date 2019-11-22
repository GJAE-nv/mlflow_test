from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
import os

your_experiment = 'ExperimentRun/' + 'type_your_expirement_here' # bijvoorbeeld: dcid.0c8c541a-4c81-4e13-b1a1-40a8ee2813de

#name of your storage account and the access key from Settings->AccessKeys->key1
block_blob_service = BlockBlobService(account_name='mlflowtest8581731198', account_key='UkSZoBB38JuL3LOZSGR/XeVJfrXds/yHFv6FlnajzOYBiYBAOvvD0nglgZowTrDUKF7v4VmZpoT0ZbRWbZWlow==')

#name of the container
generator = block_blob_service.list_blobs('azureml')

print(block_blob_service, 'block_blob_service')
print(generator, 'generator')

for blob in generator:
    print(blob.name)
    print("{}".format(blob.name))
    #check if the path contains a folder structure, create the folder structure
    if blob.name.startswith(your_experiment):
        if "/" in "{}".format(blob.name):
            print("there is a path in this")
            #extract the folder path and check if that folder exists locally, and if not create it
            head, tail = os.path.split("{}".format(blob.name))
            print(head)
            print(tail)
            if (os.path.isdir(os.getcwd()+ "/" + head)):
                #download the files to this directory
                print("directory and sub directories exist")
                block_blob_service.get_blob_to_path('azureml',blob.name,os.getcwd()+ "/" + head + "/" + tail)
            else:
                #create the diretcory and download the file to it
                print("directory doesn't exist, creating it now")
                os.makedirs(os.getcwd()+ "/" + head, exist_ok=True)
                print("directory created, download initiated")
                block_blob_service.get_blob_to_path('azureml',blob.name,os.getcwd()+ "/" + head + "/" + tail)
        else:
            block_blob_service.get_blob_to_path('azureml',blob.name,blob.name)
