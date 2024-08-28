import requests
import datetime
from elasticsearch import Elasticsearch
from cloud import Cloud
import copy
from nexenta import Nexenta
from sdi import SDI
import helper

ELASTIC_HOST    =   "127.0.0.1"

#res = requests.get('http://' + ELASTIC_HOST + ':9200')

es = Elasticsearch([{'host': ELASTIC_HOST, 'port': 9200}])

config_dict = helper.read_config_file()
site = config_dict['site']


def es_post(payload,id=None):
    index =  datetime.date.today().strftime("%Y-%m-%d-")
    index = index + site

    if id:
        output =  es.index(
            index=index,
            document=payload,
            id=id

        )
    else:
        output = es.index(
           index=index,
           document=payload
        )
    print(output)
    return output

def es_post_hypervisor(_dict):

    _hypervisor_dict_copy = copy.deepcopy(_dict)
    _hypervisor_dict_copy.pop('_hypervisor_data')
    _hypervisor_dict_copy['timestamp'] = datetime.datetime.now()
    #print(_hypervisor_dict_copy)
    #print(hypervisor_dict)

    es_post(_hypervisor_dict_copy)


    for hypervisor in _dict["_hypervisor_data"]:

        hypervisor['timestamp'] = datetime.datetime.now()
        #print(hypervisor)
        es_post(hypervisor,hypervisor['name'])


def es_post_cinder(_dict):
    _dict['timestamp'] = datetime.datetime.now()
    es_post(_dict)

sitecloud = Cloud('sitecloud')
Storage = Nexenta('sitecloud')
#
hypervisor_dict = sitecloud.total_hypervisor_resources()
cinder_dict = sitecloud.total_cinder_resources()
instance_dict = sitecloud.total_instance_resources()
nexenta_dict = Storage.get_pool()
#
es_post_cinder(instance_dict)
es_post_cinder(nexenta_dict)
es_post_cinder(cinder_dict)

es_post_hypervisor(hypervisor_dict)


def es_post_cru(_dict):
    for cru in _dict:
        cru['timestamp'] = datetime.datetime.now()
        es_post(cru,'sdi_' + cru['sdi_cru_name'])

def es_post_eas(_dict):
    for eas in _dict:
        eas['timestamp'] = datetime.datetime.now()
        es_post(eas,'sdi_' + eas['sdi_eas_name'] + eas['sdi_eas_port_id'])

def es_post_eas_count(_dict):
    _dict['timestamp'] = datetime.datetime.now()
    es_post(_dict)


sdi = SDI('sitecloud')
cru_dict = sdi.total_cru_resources()

es_post_cru(cru_dict)
es_post_cinder(sdi.get_sdi_resources_counts())

eas_dict, enableDisable = sdi.get_eas_resources_count()

es_post_eas(eas_dict['sdi_eas_LinkAdminState'])

es_post_eas_count(enableDisable)

es_post_eas_count(sdi.get_switch_count())
es_post_eas_count(sdi.get_vpod_cru_count())
