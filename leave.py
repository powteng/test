from pymysql.cursors import DictCursor
import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing
from config import *
from db_connection import db_conn, db_close

table = "holiday"
bucket = custombucket
region = customregion

def add_leave(data):

    emp_id = data['emp_id']
    start_date = data['start_date']
    end_date = data['end_date']
    total_day = data['total_day']
    reason = data['reason']

    try:
        conn = db_conn()
        cursor = conn.cursor()
        insert_sql = "INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, 0)"
        print(insert_sql)
        cursor.execute(insert_sql, (None, emp_id, start_date, end_date, total_day, reason))
        conn.commit()

    except Exception as e:
        return str(e)

    finally:
        cursor.close()
        db_close(conn)
        return "Leave Sucessfully Added"

def list_leave():
    """
    Retrieve leaves

    Returns:
        _type_: _description_
    """
    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT e.first_name, e.last_name, id, l.start_date, l.end_date, l.reason, l.total_day FROM holiday l, employee e WHERE e.emp_id = l.emp_id"  + " AND l.is_delete = 0"     
        cursor_.execute(sql)
        leaves = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return leaves

def edit_leave(data):
    print(data)
    start_date = data['start_date']
    end_date = data['end_date']
    total_day = data['total_day']
    reason = data['reason']
    leave_id = data['leave_id']

    conn = db_conn()
    cursor = conn.cursor()

    with cursor as cursor_:
        sql = "UPDATE "+ table +" SET \
        start_date = %s, \
        end_date = %s, \
        total_day = %s, \
        reason = %s \
        WHERE id = %s"

        cursor_.execute(sql, (start_date, end_date, total_day, reason, leave_id))
        conn.commit()
        cursor_.close()

    db_close(conn)    

def delete_leave(id):

    conn = db_conn()
    cursor = conn.cursor()

    with cursor as cursor_:
        sql = "UPDATE " + table + " SET is_delete = 1 WHERE id = " + str(id) 

        cursor_.execute(sql)
        conn.commit()
        cursor_.close()

    db_close(conn)

def select_leave(leave_id):

    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT e.first_name, e.last_name, id, l.start_date, l.end_date, l.reason, l.total_day FROM holiday l, employee e WHERE e.emp_id = l.emp_id AND id=" + leave_id
        cursor_.execute(sql)
        leave = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return leave[0], leave[0]['first_name'] + ' ' + leave[0]['last_name']