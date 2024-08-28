import openstack
import nova
import cinder
from datetime import datetime

class Cloud:

    def __init__(self,env):
        self.env = env
        self.conn = openstack.connect(cloud=env)
        
    def total_hypervisor_resources(self):
        hypervisor_resources = nova.hypervisor_total_resources(self.conn)
        return hypervisor_resources


    def total_cinder_resources(self):
        cinder_resources = cinder.cinder_total_resources(self.conn)
        return cinder_resources

    def total_instance_resources(self):
        instance_resources = nova.instance_total_resources(self.conn)
        return instance_resources

  #  def es_post(self):
  #      _dict = self.total_hypervisor_resource()
  #      _dict['timestamp'] = datetime.now()
  #      es.es_post(_dict)
  #              
  #      return es




#debug = Sanjose.total_memory()
#hypervisor_resources = Sanjose.total_hypervisor_resource()



#print("Total Memory :  " +  str(hypervisor_resources['total_memory']) + "   Total memory used : " + str(hypervisor_resources['total_memory_used']))