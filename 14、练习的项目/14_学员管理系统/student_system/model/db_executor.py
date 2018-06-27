# -*- coding:utf-8 -*-
from model.models import StorageServiceModel, StorageUserModel, StorageVolumeModel
from model.models import StorageMappingViewModel, StorageNfsMappingViewModel
from model import DBSession
from sqlalchemy import and_
from common.utils.exception import DatabaseError


# def retrieve_mapping_info(vol_id, user_id, to_dict=True):
#     try:
#         session = DBSession()
#         data = session.query(StorageMappingViewModel).filter(and_(StorageMappingViewModel.vol_id == int(vol_id),
#                                                                   StorageMappingViewModel.user_id == int(user_id),
#                                                                   StorageMappingViewModel.Status == "A")).first()
#         if not to_dict:
#             return data
#         if data:
#             return data.to_dict()
#     except Exception as e:
#         raise DatabaseError("retrieve mapping info failed, %s"% e.message)
#
#
# def retrieve_service_id(region, type, name, to_dict=True):
#     try:
#         session = DBSession()
#         service = session.query(StorageServiceModel).filter(and_(StorageServiceModel.region==region,
#                                                                  StorageServiceModel.type==type,
#                                                                  StorageServiceModel.name==name,
#                                                                  StorageServiceModel.Status=="A")).first()
#         if not to_dict:
#             return service
#         if service:
#             return service.to_dict()
#     except Exception as e:
#         raise DatabaseError("retrieve service id failed, %s"% e.message)


def retrieve_service(region, name, type, to_dict=False, **kwargs):
    try:
        session = DBSession()
        service = session.query(StorageServiceModel).filter(and_(StorageServiceModel.region==region,
                                                                 StorageServiceModel.name == name,
                                                                 StorageServiceModel.type==type,
                                                                 StorageServiceModel.Status=="A")).first()
        if not to_dict:
            return service
        if service:
            return service.to_dict()
    except Exception as e:
        raise DatabaseError("retrieve service failed, %s"% e.message)


def query_service_info(id=None, **kwargs):
    session = DBSession()
    if id:
        services = session.query(StorageServiceModel).filter(and_(StorageServiceModel.Id == int(id),
                                                                 StorageServiceModel.Status == "A")).first()
    else:
        services = session.query(StorageServiceModel).filter(StorageServiceModel.Status == "A").all()
    session.close()
    return services


def insert_service(region, name, type, ip, port, username, password, access_key, subnet_code=None, logic_ip=None, **kwargs):
    try:
        session = DBSession()
        service = StorageServiceModel(region=region,
                                  name=name,
                                  type=type,
                                  ip=ip,
                                  port=port,
                                  username=username,
                                  password=password,
                                  access_key=access_key,
                                  subnet_code=subnet_code,
                                  logic_ip=logic_ip)
        session.add(service)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("insert service failed, %s" % e.message)


def delete_service(id, **kwargs):
    try:
        session = DBSession()
        session.query(StorageServiceModel).filter(and_(StorageServiceModel.Id == int(id),
                                                       StorageServiceModel.Status == "A"))\
            .update({"Status": "N"}, synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("delete service failed, %s" % e.message)


def modify_service(id, **kwargs):
    try:
        session = DBSession()
        session.query(StorageServiceModel).filter(and_(StorageServiceModel.Id == int(id),
                                                       StorageServiceModel.Status == "A"))\
            .update(kwargs, synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("modify service failed, %s" % e.message)


def query_user(service_id, access_key=None, name=None, **kwargs):
    try:
        session = DBSession()
        if (name is None) and service_id and access_key:
            data = session.query(StorageUserModel).filter(and_(StorageUserModel.access_key == access_key,
                                                               StorageUserModel.service_id == int(service_id),
                                                               StorageUserModel.Status == "A")).all()
        elif (access_key is None) and service_id and name:
            data = session.query(StorageUserModel).filter(and_(StorageUserModel.name == name,
                                                               StorageUserModel.service_id == int(service_id),
                                                               StorageUserModel.Status == "A")).all()
        elif (access_key is None) and service_id and (name is None):
            data = session.query(StorageUserModel).filter(and_(StorageUserModel.service_id == int(service_id),
                                                               StorageUserModel.Status == "A")).all()
        else:
            data = session.query(StorageUserModel).filter(and_(StorageUserModel.access_key == access_key,
                                                               StorageUserModel.service_id == int(service_id),
                                                               StorageUserModel.name == name,
                                                               StorageUserModel.Status == "A")).first()
        session.close()
    except Exception as e:
        raise DatabaseError("query user failed, %s" % e.message)
    return data


def create_user(service_id, access_key, name, password, total_cap, warn_level, stor_user_id, **kwargs):
    try:
        session = DBSession()
        user = StorageUserModel(name=name,
                                password=password,
                                access_key=access_key,
                                service_id=int(service_id),
                                total_cap=total_cap,
                                warn_level=warn_level,
                                stor_user_id=stor_user_id
                                )
        session.add(user)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("create user failed, %s" % e.message)


def query_volume(service_id, access_key=None, name=None, **kwargs):
    try:
        session = DBSession()
        if (name is None) and access_key:
            data = session.query(StorageVolumeModel).filter(and_(StorageVolumeModel.access_key == access_key,
                                                                  StorageVolumeModel.service_id == int(service_id),
                                                                  StorageVolumeModel.Status == "A")).all()
        elif name and (access_key is None):
            data = session.query(StorageVolumeModel).filter(and_(StorageVolumeModel.name == name,
                                                                  StorageVolumeModel.service_id == int(service_id),
                                                                  StorageVolumeModel.Status == "A")).all()
        elif (name is None) and (access_key is None):
            data = session.query(StorageVolumeModel).filter(and_(StorageVolumeModel.service_id == int(service_id),
                                                                  StorageVolumeModel.Status == "A")).all()
        else:
            data = session.query(StorageVolumeModel).filter(and_(StorageVolumeModel.access_key == access_key,
                                                                  StorageVolumeModel.name == name,
                                                                  StorageVolumeModel.service_id == int(service_id),
                                                                  StorageVolumeModel.Status == "A")).first()
        session.close()
    except Exception as e:
        raise DatabaseError("query volume failed, %s" % e.message)
    return data


def create_volume(service_id, access_key, name, total_cap, warn_level, stor_volume_id,
                  quota_id=None, parent_dir="/", **kwargs):
    try:
        session = DBSession()
        volume = StorageVolumeModel(name=name,
                                    service_id=int(service_id),
                                    access_key=access_key,
                                    total_cap=total_cap,
                                    warn_level=warn_level,
                                    stor_volume_id=stor_volume_id,
                                    quota_id=quota_id,
                                    parent_dir=parent_dir
                                    )
        session.add(volume)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("create volume failed, %s" % e.message)


def update_user(service_id, access_key, name, password, total_cap=None, warn_level=None, **kwargs):
    try:
        session = DBSession()
        if total_cap and warn_level:
            session.query(StorageUserModel).filter(and_(StorageUserModel.service_id==int(service_id),
                                                        StorageUserModel.access_key==access_key,
                                                        StorageUserModel.name==name,
                                                        StorageUserModel.Status == "A")).update({"password":password,
                                                                                                "total_cap":total_cap,
                                                                                                "warn_level":warn_level},
                                                                                                synchronize_session=False)
        session.commit()
        session.close()

    except Exception as e:
        raise DatabaseError("update user failed, %s" % e.message)


def delete_user(service_id, access_key, name, **kwargs):
    try:
        session = DBSession()
        user = session.query(StorageUserModel).filter(and_(StorageUserModel.service_id==int(service_id),
                                                           StorageUserModel.access_key==access_key,
                                                           StorageUserModel.name==name,
                                                           StorageUserModel.Status=="A")).update({"Status":"N"},
                                                                                         synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("delete user failed, %s" % e.message)


def update_volume(service_id, access_key, name, total_cap, warn_level, **kwargs):
    try:
        session = DBSession()
        user = session.query(StorageVolumeModel).filter(and_(StorageVolumeModel.service_id==int(service_id),
                                                             StorageVolumeModel.access_key==access_key,
                                                             StorageVolumeModel.name==name,
                                                             StorageVolumeModel.Status=="A")).update({"total_cap":total_cap,
                                                                                              "warn_level":warn_level},
                                                                                            synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("update volume failed, %s" % e.message)


def delete_volume(service_id, access_key, name, **kwargs):
    try:
        session = DBSession()
        user = session.query(StorageVolumeModel).filter(and_(StorageVolumeModel.service_id==int(service_id),
                                                             StorageVolumeModel.access_key==access_key,
                                                             StorageVolumeModel.name==name,
                                                             StorageVolumeModel.Status=="A")).update({"Status":"N"},
                                                                                             synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("delete volume failed, %s" % e.message)


def create_mapping(vol_id, user_id, share_id, share_client_id, share_point_name, share_path, limit, **kwargs):
    try:
        session = DBSession()
        mapping = StorageMappingViewModel(vol_id=int(vol_id),
                                       user_id=int(user_id),
                                       share_id=share_id,
                                       share_client_id= share_client_id,
                                       share_point_name=share_point_name,
                                       share_path=share_path,
                                       limit=limit)
        session.add(mapping)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("create mapping failed, %s" % e.message)


def query_mapping(vol_id=None, user_id=None, **kwargs):
    try:
        session = DBSession()
        if (vol_id is None) and user_id:
            data = session.query(StorageMappingViewModel).filter(and_(StorageMappingViewModel.user_id == int(user_id),
                                                                      StorageMappingViewModel.Status == "A")).all()
        elif (user_id is None) and vol_id:
            data = session.query(StorageMappingViewModel).filter(and_(StorageMappingViewModel.vol_id == int(vol_id),
                                                                      StorageMappingViewModel.Status == "A")).all()
        elif vol_id and user_id:
            data = session.query(StorageMappingViewModel).filter(and_(StorageMappingViewModel.vol_id == int(vol_id),
                                                                      StorageMappingViewModel.user_id == int(user_id),
                                                                      StorageMappingViewModel.Status == "A")).first()
        else:
            data = session.query(StorageMappingViewModel).filter(StorageMappingViewModel.Status == "A").all()
        session.close()
    except Exception as e:
        raise DatabaseError("query mapping failed, %s" % e.message)
    return data


# def query_mapping_by_volume(service_id, access_key, volume_name):
#     try:
#         session = DBSession()
#         vol_id = query_volume(int(service_id), access_key, volume_name)["Id"]
#         data = session.query(StorageMappingViewModel).filter(and_(StorageMappingViewModel.vol_id==vol_id,
#                                                                   StorageMappingViewModel.Status=="A")).all()
#         session.close()
#         return [d.to_dict() for d in data]
#     except Exception as e:
#         raise DatabaseError("query mapping failed, %s" % e.message)


def delete_mapping(vol_id, user_id, **kwargs):
    try:
        session = DBSession()
        session.query(StorageMappingViewModel).filter(and_(StorageMappingViewModel.vol_id==int(vol_id),
                                                           StorageMappingViewModel.user_id==int(user_id),
                                                           StorageMappingViewModel.Status=="A")).update({"Status":"N"},
                                                                                        synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("delete mapping failed, %s" % e.message)


def update_mapping(vol_id, user_id, limit, **kwargs):
    try:
        session = DBSession()
        session.query(StorageMappingViewModel).filter(and_(StorageMappingViewModel.vol_id==int(vol_id),
                                                           StorageMappingViewModel.user_id==int(user_id),
                                                           StorageMappingViewModel.Status=="A")).update({"limit":limit},
                                                                                        synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("change mapping failed, %s" % e.message)


def create_nfs_mapping(vol_id, client_ip, share_id, share_path, share_client_id, limit, **kwargs):
    try:
        session = DBSession()
        mapping = StorageNfsMappingViewModel(vol_id=int(vol_id),
                                           client_ip = client_ip,
                                           share_id=share_id,
                                           share_path=share_path,
                                           share_client_id = share_client_id,
                                           limit = limit)
        session.add(mapping)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("create mapping failed, %s" % e.message)


def query_nfs_mapping(vol_id=None, client_ip=None, **kwargs):
    try:
        session = DBSession()
        if (vol_id is None) and client_ip:
            data = session.query(StorageNfsMappingViewModel).filter(and_(StorageNfsMappingViewModel.client_ip == client_ip,
                                                                         StorageNfsMappingViewModel.Status == "A")).all()
        elif (client_ip is None) and vol_id:
            data = session.query(StorageNfsMappingViewModel).filter(and_(StorageNfsMappingViewModel.vol_id == int(vol_id),
                                                                         StorageNfsMappingViewModel.Status == "A")).all()
        elif vol_id and client_ip:
            data = session.query(StorageNfsMappingViewModel).filter(and_(StorageNfsMappingViewModel.vol_id == int(vol_id),
                                                                         StorageNfsMappingViewModel.client_ip == client_ip,
                                                                         StorageNfsMappingViewModel.Status == "A")).first()
        else:
            data = session.query(StorageNfsMappingViewModel).filter(StorageNfsMappingViewModel.Status == "A").all()
        session.close()
    except Exception as e:
        raise DatabaseError("query mapping failed, %s" % e.message)
    return data


# def query_nfs_mapping_by_volume(service_id, access_key, volume_name):
#     try:
#         session = DBSession()
#         vol_id = query_volume(int(service_id), access_key, volume_name)["Id"]
#         data = session.query(StorageNfsMappingViewModel).filter(and_(StorageNfsMappingViewModel.vol_id == vol_id,
#                                                                      StorageNfsMappingViewModel.Status == "A")).all()
#         session.close()
#         return [d.to_dict() for d in data]
#     except Exception as e:
#         raise DatabaseError("query mapping failed, %s" % e.message)


def delete_nfs_mapping(vol_id, client_ip, **kwargs):
    try:
        session = DBSession()
        session.query(StorageNfsMappingViewModel).filter(and_(StorageNfsMappingViewModel.vol_id == int(vol_id),
                                                              StorageNfsMappingViewModel.client_ip == client_ip,
                                                              StorageNfsMappingViewModel.Status == "A"))\
            .update({"Status": "N"}, synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("delete mapping failed, %s" % e.message)


def update_nfs_mapping(vol_id, client_ip, limit, **kwargs):
    try:
        session = DBSession()
        session.query(StorageNfsMappingViewModel).filter(and_(StorageNfsMappingViewModel.vol_id == int(vol_id),
                                                              StorageNfsMappingViewModel.client_ip == client_ip,
                                                              StorageNfsMappingViewModel.Status == "A"))\
            .update({"limit": limit}, synchronize_session=False)
        session.commit()
        session.close()
    except Exception as e:
        raise DatabaseError("change mapping failed, %s" % e.message)




