import os
import argparse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from dotenv import load_dotenv

load_dotenv('/home/nus/iperf/scripts/.env')

parser = argparse.ArgumentParser(description='')
parser.add_argument('--name', '-n', default=None, type=str, help='node identifier')
args = parser.parse_args()

container_name = 'traces'
local_path = '/home/nus/logs/'
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

for file_name in os.listdir(local_path):
    upload_file_path = os.path.join(local_path, file_name)
    if not file_name.endswith('.log'):
        continue
    if os.path.getsize(upload_file_path) == 0:
        os.remove(upload_file_path)
        continue
    try:
        upname = f'{args.name}-{file_name}'
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=upname)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
        os.remove(upload_file_path)
    except Exception as ex:
        print('Exception:')
        print(ex)
