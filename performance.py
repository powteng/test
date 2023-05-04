from pymysql.cursors import DictCursor
from config import *
from db_connection import db_conn, db_close

table = "performance"
bucket = custombucket
region = customregion

def add_perf(data):
    
    emp_id = data['emp_id']
    course = data['course']
    grade = data['grade']
    performance = data['performance']
    score = data['score']

    try:
        conn = db_conn()
        cursor = conn.cursor()
        insert_sql = "INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, 0)"
        print(insert_sql)
        cursor.execute(insert_sql, (None, emp_id, score, grade, performance, course))
        conn.commit()

    except Exception as e:
        return str(e)

    finally:
        cursor.close()
        return "perf Sucessfully Added"

def list_perf():
    """
    Retrieve perfs

    Returns:
        _type_: _description_
    """
    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT e.first_name, e.last_name, p.id, grade, performance, score, course_id, c.course_name \
                FROM performance p, employee e, course c \
                WHERE e.emp_id = p.emp_id \
                AND p.course_id = c.id \
                AND p.is_delete = 0"

        cursor_.execute(sql)
        perfs = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return perfs

def edit_perf(data):
    print(data)
    emp_id = data['emp_id']
    course_id = data['course_id']
    grade = data['grade']
    performance = data['performance']
    score = data['score']
    perf_id = data['perf_id']

    conn = db_conn()
    cursor = conn.cursor()

    with cursor as cursor_:
        sql = "UPDATE "+ table +" SET \
        course_id = %s, \
        grade = %s, \
        performance = %s, \
        score = %s \
        WHERE id = %s"

        cursor_.execute(sql, (course_id, grade, performance, score, perf_id))
        conn.commit()
        cursor_.close()

    db_close(conn)    

def delete_perf(id):

    conn = db_conn()
    cursor = conn.cursor()

    with cursor as cursor_:
        sql = "UPDATE " + table + " SET is_delete = 1 WHERE id = " + str(id) 

        cursor_.execute(sql)
        conn.commit()
        cursor_.close()

    db_close(conn)

def select_perf(perf_id):

    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT p.id, e.first_name, e.last_name, p.course_id, p.score, p.grade, p.performance, c.course_name \
            FROM performance p, employee e, course c \
            WHERE c.id = p.course_id \
            AND e.emp_id = p.emp_id AND p.id= " + perf_id
        cursor_.execute(sql)
        perf = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return perf[0], perf[0]['first_name'] + ' ' + perf[0]['last_name']

def list_course():
    """
    Retrieve perfs

    Returns:
        _type_: _description_
    """
    conn = db_conn()
    cursor = conn.cursor(DictCursor)

    with cursor as cursor_:
        sql = "SELECT * FROM course"     
        cursor_.execute(sql)
        courses = cursor.fetchall()
        cursor_.close()

    db_close(conn)

    return courses