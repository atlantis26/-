from core.orm import ResourcePool, School
from conf.settings import ResourcePoolDir
from core.db_handler import load_pkl
import os


def init_resource_pool():
    """初始化系统，新建学校等对象，如果对象已被创建保存，则通过pickle重构对象"""
    resource_pool_file = os.path.join(ResourcePoolDir, "ResourcePool.pkl")
    if os.path.exists(resource_pool_file):
        rp = load_pkl(resource_pool_file)
    else:
        rp = ResourcePool()
        beijing = School("beijing")
        beijing.create_course("linux", 365, 5000)
        beijing.create_course("python", 365, 6000)
        beijing.create_class(u"1班", "linux")
        beijing.create_class(u"2班", "python")

        shanghai = School("beijing")
        shanghai.create_course("go", 365, 6000)
        shanghai.create_class(u"1班", "go")

        beijing.create_teacher("alex", [u"1班"])
        beijing.create_teacher("jack", [u"2班"])
        shanghai.create_teacher("lucy", [u"1班"])
        rp.schools.extend([beijing, shanghai])

    return rp
