


def hypervisor_total_resources(conn):
    _dict = []
    _hypervisor_dict = []
    total_memory = 0
    total_memory_used = 0
    total_vcpu = 0
    total_vcpu_used = 0
    hypervisor_count = 0
    active_hypervisor_count = 0

    hypervisors = conn.compute.hypervisors(details=True)
    for hypervisor in hypervisors:    
        hypervisor_count += 1
        if hypervisor.status == 'enabled':
            active_hypervisor_count += 1
            total_memory += hypervisor.memory_size
            total_memory_used += hypervisor.memory_used
            total_vcpu += hypervisor.vcpus
            total_vcpu_used += hypervisor.vcpus_used
          
        data = {
            'name'      :   hypervisor.name,
            'vcpu'      :   hypervisor.vcpus,
            'vcpu_used' :   hypervisor.vcpus_used,
            'vcpu_used_percentage'  :   hypervisor.vcpus_used / hypervisor.vcpus * 100,
            'memory'    :   hypervisor.memory_size,
            'memory_used':  hypervisor.memory_used,
            'memory_used_percentage' :  hypervisor.memory_used / hypervisor.memory_size * 100,
            'running_vms':  hypervisor.running_vms,
            'status'    :   hypervisor.status
            
        }
        _hypervisor_dict.append(data)
    
    _dict = {
        'total_memory'      : total_memory,
        'total_memory_used' : total_memory_used,
        'total_vcpu'        : total_vcpu,
        'total_vcpu_used'   : total_vcpu_used,
        'total_hypervisor'  : hypervisor_count,
        'active_hypervisors' : active_hypervisor_count,
        '_hypervisor_data'  : _hypervisor_dict
    }
    
    return _dict



def instance_total_resources(conn):
    _dict = []    
    instance_count = 0

    instances = conn.compute.servers(details=True,all_projects=True)
    for instance in instances:
        instance_count += 1

    _dict = {
        'vm_count' : instance_count
    }

    return _dict





