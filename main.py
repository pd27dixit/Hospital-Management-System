import MySQLdb.cursors
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import numpy as np
from datetime import datetime
import math

now = datetime.now().strftime('%H:%M')

app = Flask(__name__)
app.secret_key = 'the random string'

app.config['MYSQL_HOST'] = '10.5.18.69'
app.config['MYSQL_USER'] = '20CS10047'
app.config['MYSQL_PASSWORD'] = '20CS10047'
app.config['MYSQL_DB'] = '20CS10047'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        if session["username"] == "admin":
            return redirect("/index")
        else:
            return redirect("/patient_appointment")
    msg = ""
    if request.method == 'GET':
        if request.form.get("username") is None:
            return render_template('login.html')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM login")
    data = cursor.fetchall()
    for item in data:
        assert isinstance(item, object)

    for item in data:
        username = item['loginname']
        password = item['password']
        user=item['userid']
        session["username"] = username
        session["user"]= user
        if request.method == 'POST':
            if username == request.form.get("username"):
                if password != request.form.get("password"):
                    msg = "Please Enter Correct Password"
                    flash(msg)
                    return render_template('login.html')

                else:
                    if username == 'admin':
                        return redirect(url_for('index'))
                    elif username == 'sahil':
                        return redirect("/patient_appointment")
                    return render_template('login.html')


@app.route('/logout',)
def logout():
    session.pop("username", None)
    session.pop("user", None)
    return redirect("/login")


@app.route("/index")
def index():
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT COUNT(*) FROM patient")
            count = cursor.fetchall()
            attend = np.random.randint(0, count[0]['COUNT(*)'] + 1)
            pend = count[0]['COUNT(*)'] - attend

            cursor.execute("SELECT COUNT(*) FROM doctor")
            count_doc = cursor.fetchall()
            cursor.execute("SELECT * FROM doctor")
            doctor = cursor.fetchall()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT * FROM patient")
            patient = cursor.fetchall()

            cursor.execute(
                "SELECT * FROM appointment order by appointmentdate")
            appointment = cursor.fetchall()

            return render_template('index.html', count=count, count_doc=count_doc, attend=attend, pend=pend, doctor=doctor, patient=patient, appointment=appointment)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/doctors")
def doctors():
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT * FROM doctor")
            doctor = cursor.fetchall()

            return render_template('doctors.html', doctor=doctor)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/add_doctor")
def add_doctor():
    if "user" in session:
        if session["username"] == "admin":
            return render_template('add-doctor.html')
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/adddoctor", methods=['GET', 'POST'])
def adddoctor():
    if "user" in session:
        if session["username"] == "admin":
            if request.method == 'POST':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                name = request.form.get("name")
                phone = request.form.get("phone")
                gender = request.form.get("gender")
                education = request.form.get("education")
                department = request.form.get("department")
                experience = request.form.get("exp")
                consultancy_charge = request.form.get("charge")
                status = request.form.get("status")
                start_time = request.form.get("starttime")
                end_time = request.form.get("endtime")
                cursor.execute("INSERT INTO doctor (doctorname, mobileno,departmentname,status,education,experience,consultancy_charge,gender,start_time,end_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s')" % (
                    name, phone, department, status, education, experience, consultancy_charge, gender, start_time, end_time))
                mysql.connection.commit()
                return redirect("/doctors")
            else:
                return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/deletedoctor/<int:doctorid>")
def deletedoctor(doctorid):
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "DELETE from doctor where doctorid='%d'" % (doctorid))
            mysql.connection.commit()
            return redirect('/doctors')
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/appointments")
def appointments():
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute(
                "SELECT * FROM appointment order by appointmentdate ")
            app = cursor.fetchall()
            return render_template('appointments.html', app=app)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/editappointment/<int:appointmentid>")
def editappointment(appointmentid):
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            row = cursor.execute(
                "SELECT * FROM appointment where appointmentid='%d'" % appointmentid)
            row = cursor.fetchone()
            if row['status'] == "Active":
                cursor.execute("UPDATE appointment SET status='%s' WHERE appointmentid='%s'" % (
                    "Inactive", (appointmentid)))
            else:
                cursor.execute("UPDATE appointment SET status='%s' WHERE appointmentid='%s'" % (
                    "Active", (appointmentid)))
            mysql.connection.commit()

            return redirect('/appointments')
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/patients")
def patients():
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT * FROM patient")
            patient = cursor.fetchall()
            return render_template('patients.html', patient=patient)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/add_patient")
def add_patient():
    if "user" in session:
        if session["username"] == "admin":
            return render_template('add-patient.html')
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/addpatients", methods=['GET', 'POST'])
def addpatients():
    if "user" in session:
        if session["username"] == "admin":
            if request.method == 'POST':

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                name = request.form.get("name")
                email = request.form.get("email")
                age = request.form.get("age")
                blood_group = request.form.get("blood-group")
                gender = request.form.get("gender")
                address = request.form.get("address")
                city = request.form.get("city")
                pincode = request.form.get("pincode")
                phone = request.form.get("phone")
                illness = request.form.get("illness")
                cursor.execute("INSERT INTO patient (patientname,email,address, mobileno,city,pincode,bloodgroup,gender,age,illness) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                    name, email, address, phone, city, pincode, blood_group, gender, age, illness))
                mysql.connection.commit()
                return redirect("/patients")
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/deletepatient/<int:patientid>")
def deletepatient(patientid):
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "DELETE from patient where patientid='%d'" % (patientid))
            mysql.connection.commit()
            return redirect('/patients')
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/schedule")
def schedule():
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT * FROM doctor")
            schedule = cursor.fetchall()
            return render_template('schedule.html', schedule=schedule, now=now)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/departments")
def departments():
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT * FROM department")
            department = cursor.fetchall()
            return render_template('departments.html', department=department)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/editdepartment/<int:departmentid>")
def editdepartment(departmentid):
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            row = cursor.execute(
                "SELECT * FROM department where departmentid='%d'" % departmentid)
            row = cursor.fetchone()
            if row['status'] == "Active":
                cursor.execute("UPDATE department SET status='%s' WHERE departmentid='%s'" % (
                    "Inactive", (departmentid)))
            else:
                cursor.execute("UPDATE department SET status='%s' WHERE departmentid='%s'" % (
                    "Active", (departmentid)))
            mysql.connection.commit()

            return redirect('/departments')
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/addappointment")
def addappointment():
    if "user" in session:
        if session["username"] == "sahil":
            return render_template('add-appointment.html')
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/patient_appointment", methods=['GET', 'POST'])
def patient_appointment():
    if "user" in session:
        if session["username"] == "sahil":
            msg = ""

            if request.method == 'POST':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                name = request.form.get("name")
                department = request.form.get("department")
                doctor = request.form.get("doctor")
                date = request.form.get("date")
                time = request.form.get("time")
                email = request.form.get("email")

                phone = request.form.get("phoneno")
                messg = request.form.get("messg")
                cursor.execute("INSERT INTO appointment (patientname,departmentname,doctorname,appointmentdate,appointmenttime,phone,email,message) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                    name, department, doctor, date, time, email, phone, messg))
                mysql.connection.commit()
                msg = "Appointment is Scheduled"
                flash(msg)
                return redirect("/patient_appointment")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM doctor")
            doctor = cursor.fetchall()
            cursor.execute("SELECT * FROM department")
            department = cursor.fetchall()

            return render_template('appointment.html', doctor=doctor, department=department)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/invoices")
def invoices():
    if "user" in session:
        if session["username"] == "admin":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM billing")
            bills = cursor.fetchall()
            return render_template('invoices.html', bills=bills,)
        else:
            return redirect("/logout")
    else:
        return redirect("/login")


@app.route("/invoicesbill/<int:billingid>")
def invoicesbill(billingid):
    if "user" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM  billing where billingid='%d'" % billingid)
        row = cursor.fetchone()
        cursor.execute(
            "SELECT * FROM  appointment where patientname='%s'" % row['patientname'])
        patientname = cursor.fetchone()
        cursor.execute("SELECT * FROM  doctor where doctorname='%s'" %
                       patientname['doctorname'])
        doctor = cursor.fetchone()
        medi = np.random.randint(10000, 20000)
        print(doctor['consultancy_charge'])
        sub = float(doctor['consultancy_charge']) + medi + 5000
        tax = np.random.randint(10, 25)
        taxamt = math.trunc(sub * (tax/100))
        grand = taxamt + sub
        return render_template("invoice-bill.html", row=row, doctor=doctor, medical=medi, grand=grand, taxamt=taxamt, tax=tax)
    else:
        return redirect("/login")


@app.route("/invoices_bill")
def invoices_bill():
    if "user" in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM  billing where patientname='%s'" % session['username'])
        row = cursor.fetchone()
        cursor.execute(
            "SELECT * FROM  appointment where patientname='%s'" % row['patientname'])
        patientname = cursor.fetchone()
        cursor.execute("SELECT * FROM  doctor where doctorname='%s'" %
                       patientname['doctorname'])
        doctor = cursor.fetchone()
        medi = np.random.randint(10000, 20000)
        print(doctor['consultancy_charge'])
        sub = float(doctor['consultancy_charge']) + medi + 5000
        tax = np.random.randint(10, 25)
        taxamt = math.trunc(sub * (tax/100))
        grand = taxamt + sub
        return render_template("invoice-bill.html", row=row, doctor=doctor, medical=medi, grand=grand, taxamt=taxamt, tax=tax)
    else:
        return redirect("/login")


app.run(debug=True)
