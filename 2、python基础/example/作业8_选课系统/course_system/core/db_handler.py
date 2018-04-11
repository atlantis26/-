# coding:utf-8
import pickle


def load_pkl(obj_pkl):
    """文件读取对象pkl字符串，并重构存储对象"""
    with open(obj_pkl, 'r') as f:
        obj = pickle.load(f)
    return obj


def save_pkl(obj):
    """文件存储保存对象"""
    pkl_string = pickle.dumps(obj)
    with open("", "w") as f:
        f.write(pkl_string)
