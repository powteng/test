from flask import Flask, render_template, request, redirect
import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.handlers import disable_signing

from config import *
from employee import add_employee, edit_employee, list_employee, delete_employee, select_employee
from leave import add_leave, delete_leave, edit_leave, list_leave, delete_leave, select_leave
from performance import add_perf, delete_perf, edit_perf, list_perf, delete_perf, select_perf, list_course

app = Flask(__name__)

bucket = custombucket
region = customregion

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/portfolio", methods=['GET'])
def portfolio():
    return render_template('portfolio.html')

""" leave Link Start"""
@app.route("/add_leave", methods=['GET'])
def showAddLeaveForm():

    return render_template('leave/leave.html', leave=None, employees=list_employee())

@app.route("/edit_leave/<id>", methods=['GET'])
def showEditLeaveForm(id):

    leave, name = select_leave(id)
    return render_template('leave/edit_leave.html', leave=leave, name=name)

@app.route("/edit_leave_post", methods=['POST'])
def editLeaveFormPost():
    edit_leave(request.form)
    return redirect('/list_leave')  
    
@app.route("/delete_leave/<id>", methods=['GET'])
def delLeave(id):
    delete_leave(id)
    return redirect('/list_leave')

@app.route("/add_leave_post", methods=['POST'])
def addLeave():

    return render_template('leave/AddLeaveFormOutput.html', name=add_leave(request.form))

@app.route("/list_leave", methods=['GET'])
def listLeave():

    return render_template('leave/list_leave.html', leaves=list_leave())
""" leave Link End"""

""" Employee Link Start"""
@app.route("/add_emp", methods=['GET'])
def showAddEmpForm():

    return render_template('employee/AddEmpForm.html', employee=None)

@app.route("/edit_emp/<id>", methods=['GET'])
def showEditEmpForm(id):

    return render_template('employee/EditEmpForm.html', employee=select_employee(id))

@app.route("/edit_emp_post", methods=['POST'])
def editEmpFormPost():
    edit_employee(request.form)
    return redirect('/list_emp')    


@app.route("/delete_emp/<id>", methods=['GET'])
def delEmp(id):
    delete_employee(id)
    # return redirect(serverurl + '/list_emp')
    return redirect('/list_emp')    

@app.route("/add_emp_post", methods=['POST'])
def addEmp():
    fn = request.form['first_name']
    ln = request.form['last_name']
    po = request.form['position']
    em = request.form['email']
    ge = request.form['gender']
    ph = request.form['phone']
    photo = request.files['photo']
    ic = request.files['ic']

    return render_template('employee/AddEmpFormOutput.html', name=add_employee(fn, ln, po, em, ge, ph, photo, ic))

@app.route("/list_emp", methods=['GET'])
def listEmp():

    return render_template('employee/ListEmp.html', employees=list_employee())
""" Employee Link End"""

""" perf Link Start"""
@app.route("/add_perf", methods=['GET'])
def showAddPerfForm():

    return render_template('perf/perf.html', perf=None, employees=list_employee(), courses=list_course())

@app.route("/edit_perf/<id>", methods=['GET'])
def showEditPerfForm(id):

    perf, name = select_perf(id)
    return render_template('perf/edit_perf.html', perf=perf, name=name)

@app.route("/edit_perf_post", methods=['POST'])
def editPerfFormPost():
    edit_perf(request.form)
    return redirect('/list_perf')  
    
@app.route("/delete_perf/<id>", methods=['GET'])
def delPerf(id):
    delete_perf(id)
    return redirect('/list_perf')

@app.route("/add_perf_post", methods=['POST'])
def addPerf():

    return render_template('perf/AddPerfFormOutput.html', name=add_perf(request.form))

@app.route("/list_perf", methods=['GET'])
def listPerf():

    return render_template('perf/list_perf.html', perfs=list_perf())
""" perf Link End"""

@app.route("/list_course", methods=['GET'])
def listCourse():

    return render_template('course/list_course.html', courses=list_course())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
