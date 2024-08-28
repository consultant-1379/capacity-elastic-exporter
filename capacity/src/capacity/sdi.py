import helper
from helper import get_url
import datetime

class SDI:

    def __init__(self,env):
        self.env = env
        config_dict = helper.read_config_file()
        self.sdi_config = config_dict['clouds'][env]['Sdi']
        
    def get_cru_count(self):
        cru_data = self.sdi_config['cru_data']
        return len(cru_data) + 2  # Add 2 for RTE count

    def get_cru_number(self,id):
        cru_data = self.sdi_config['cru_data']
        if id in cru_data.keys():
            return cru_data[id]['cru_number']
        else:
            return 'NA'

    def get_cru_rack_unit(self,id):
        cru_data = self.sdi_config['cru_data']
        if id in cru_data.keys():
            return cru_data[id]['rack_unit']
        else:
            return 'NA'

    
    def total_cru_resources(self):
        base_url = self.sdi_config['api_url']
        api_url = base_url + '/rest/v0/Systems'

        crus = get_url(api_url,self.sdi_config)

        _list = []
        for cru in crus['Links']['Members']:
            
            cru_data = get_url(base_url + cru['@odata.id'],self.sdi_config)
            Vpod     = get_url(base_url + cru_data['Links']['VPod']['@odata.id'],self.sdi_config)
            _data = {
                'sdi_cru_name'           : cru_data['Name'],
                'sdi_cru_id'             : cru_data['Id'],
                'sdi_cru_powerstate'     : cru_data['PowerState'],
                'sdi_cru_status'         : cru_data['Status']['State'],
                'sdi_cru_model'          : cru_data['Model'],
                'sdi_cru_number'         : self.get_cru_number(cru_data['Id']),
                'sdi_cru_vpod'           : Vpod['Name'],
                'sdi_cru_serial_number'   : cru_data['SerialNumber'],
                'sdi_cru_part_number'     : cru_data['PartNumber'],
                'sdi_rack_unit'          : self.get_cru_rack_unit(cru_data['Id'])
            }
            print(_data['sdi_rack_unit'])

            _list.append(_data)

        return _list

    def get_vpod_count(self):
        base_url = self.sdi_config['api_url']
        api_url  =  base_url + '/rest/v0/VPodAdminService/VPods'
        vpods = get_url(api_url,self.sdi_config)
        vpod_count = len(vpods['Links']['Members'])
        return vpod_count

    def get_sdi_resources_counts(self):

        _dict = {}
        _dict['sdi_cru_count']      = self.get_cru_count()
        _dict['sdi_vpod_count']       = self.get_vpod_count()

        return _dict

    def total_eas_resources(self):
        base_url = self.sdi_config['api_url']
        api_url = base_url + '/rest/v0/PhysicalSwitches'
        easurl = get_url(api_url,self.sdi_config)
        nDisabled = 0
        _list = []
        for eas in easurl['Links']['Members']:

            eas_data = get_url(base_url + eas ['@odata.id'] + '/PhysicalPorts?$top=200' + '',self.sdi_config)
            portname    = get_url(base_url + eas['@odata.id'],self.sdi_config)
            values = eas_data.get('Links')['Members']
            for node in values:
                ports    = get_url(base_url + node['@odata.id'],self.sdi_config)
                _data = {
                'sdi_eas_name'           : portname['Name'],
                'sdi_eas_port_id'           : ports['Id'],
                'sdi_eas_LinkAdminState'      : ports['LinkAdminState'],
                'sdi_eas_LinkState'      : ports['LinkState'],
                }
                if _data['sdi_eas_LinkAdminState']=="Disabled":
                        nDisabled+=1
                #print(_data ['sdi_eas_name'])
                _list.append(_data)
        status = (len(_list)-nDisabled,nDisabled)
        return _list, status
        
    def get_eas_resources_count(self):

        _dict = {}
        _dict2 = {}
        _dict['sdi_eas_LinkAdminState'],_dict['EnableDisable'] = self.total_eas_resources()
        _dict2 = {
                    'ports_enable_count' : int(_dict["EnableDisable"][0]),
                    'ports_disable_count' : int(_dict["EnableDisable"][1]),
                }
        return _dict, _dict2

    def total_switch(self):
        base_url = self.sdi_config['api_url']
        api_url = base_url + '/rest/v0/PhysicalSwitches'

        phsw = get_url(api_url,self.sdi_config)
        nType = 0
        nCon  = 0
        _list = []
        for sw in phsw['Links']['Members']:

            cru_data = get_url(base_url + sw['@odata.id'],self.sdi_config)
            _data = {
                'sdi_nw_type'           : cru_data['NetworkType'],
            }
            if _data['sdi_nw_type']=="Data":
                    nType+=1
            elif _data['sdi_nw_type']=="Control":
                    nCon+=1
            _list.append(_data)
        net_type = (len(_list)-nType,nType)
        net_Con = (len(_list)-nCon,nCon)
        return _list, net_type, net_Con

    def get_switch_count(self):

        _dict = {}
        _dict2 = {}
        _dict['sdi_nw_type'],_dict['net_type'],_dict['net_Con'] = self.total_switch()
        _dict2 = {
                  'sdi_data_sw_count' : int(_dict["net_type"][1]),
                  'sdi_control_sw_count' : int(_dict["net_Con"][1]),
                 }
        return _dict2

    def total_cru_vpod(self):
        base_url = self.sdi_config['api_url']
        api_url = base_url + '/rest/v0/VPodAdminService/VPods'
        podurl = get_url(api_url,self.sdi_config)
        _list = []
        for pods in podurl['Links']['Members']:

            vpod_name = get_url(base_url + pods['@odata.id'],self.sdi_config)
            vpod_cru_count   = get_url(base_url + pods['@odata.id'] +  '/ComputerSystems',self.sdi_config)
            _data = {
                    (vpod_name['Description'])          : len(vpod_cru_count['Links']['Members']),
                    }
            _list.append(_data)
        return _list

    def get_vpod_cru_count(self):

        _dict = {}
        _dict = self.total_cru_vpod()
        _dict = {
                'vpod_data' : _dict,
                }
        return _dict

#myClass = SDI('siteclnud')
#my.total_eas_resources()

#print(nodes,enabledDisabled)
#Sanjose = SDI('Sanjose')
#Sanjose.get_vpod_count()
#print(Sanjose.get_vpod_count())
##Sanjose.get_cru_count()
#print(Sanjose.get_cru_number('15237c9c-50ea-11ea-89d2-98a404224ff0'))
#print(Sanjose.total_cru_resources())



 
