import requests
import yaml
import math
class Nexenta:


    def __init__(self,env):
        self.env = env
        
        with open('clouds.yaml') as file:

            storage_config = yaml.load(file, Loader=yaml.FullLoader)['clouds'][env]['Storage']
        

        self.api_url     = storage_config['api_url']
        self.auth_token  = self.get_auth_token(storage_config)
       
    

    def rest_get(self,url,_headers=None):
        response = requests.get(url,headers=_headers,verify=False)
        return response.json()

    def get_auth_token(self,storage_config):
        auth_url = storage_config['api_url'] + '/auth/login'
        storage_config.pop('api_url')
        response = requests.post(auth_url, data=storage_config,verify=False)
        return response.json()['token']

    def get_pool(self):
        _dict = []
        headers = {"Authorization": "Bearer "+ self.auth_token}
        url = self.api_url + '/storage/pools'
        response = self.rest_get(url,headers)
        # Coverting bytes to gb
        _dict = {
            'total_volume_size' : response['data'][0]['size'] /1024.0**3
        }
        return _dict
