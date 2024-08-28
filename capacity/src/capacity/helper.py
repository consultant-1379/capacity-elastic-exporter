import requests
import yaml
from requests.auth import HTTPBasicAuth


DEFAULT_API_HEADER = {'content-type': 'application/json'}

def read_config_file():
    with open('clouds.yaml') as file:
       config_data = yaml.load(file, Loader=yaml.FullLoader)
    return config_data

def get_url(url,auth):
    username, password = auth['username'], auth['password']
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=DEFAULT_API_HEADER, verify=False)
    return response.json()