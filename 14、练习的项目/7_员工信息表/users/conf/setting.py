# coding:utf-8
import os

DB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
StaffTable = os.path.join(DB_DIR, "db", "staff_table.txt")
StaffFields = ["staff_id", "name", "age", "phone", "dept", "enroll_date"]