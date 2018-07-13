# coding:utf-8
from core.main import console
from db import create_tables

# 初始化数据库
create_tables()

if __name__ == '__main__':
    console()
