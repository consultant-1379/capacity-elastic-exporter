


def cinder_total_resources(conn):
    _dict = []
    total_used_volume = 0
    vol_count         = 0
    volumes = conn.block_storage.volumes(details=True,all_projects=True)
    
    for volume in volumes:
        vol_count   += 1
        total_used_volume += volume.size
    _dict = {
        'total_used_volume' : total_used_volume,
        'volume_count'      : vol_count
    }
    
    print(_dict)
    return _dict


