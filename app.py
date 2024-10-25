import os
from flask import Flask, render_template, request, redirect, url_for
os.add_dll_directory(r"D:\Python_cua_toi\.venv\Lib\site-packages\clidriver\bin")
import ibm_db


app = Flask(__name__)
# Set your IBM Db2 credentials in the environment variables or manually assign them in the code below.
dsn_hostname = os.getenv('DB_HOST',
                         'ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud')  # change this
dsn_uid = os.getenv('DB_UID', 'cmg46328')  # change this
dsn_pwd = os.getenv('DB_PWD', 'RhUKhnpO9UgOncgh')  # change this
dsn_port = os.getenv('DB_PORT', '31505')  # change this
dsn_database = "bludb"  # change if necessary
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

# Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,
                            dsn_security)


# Kết nối DB2 với Flask
def connect_db2():
    # conn_str = "DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;PROTOCOL=TCPIP;UID=cmg46328;PWD=RhUKhnpO9UgOncgh;"

    try:
        conn = ibm_db.connect(dsn, "", "")  # could change conn_str
        print("Connected to database")
        return conn
    except:
        print("Unable to connect to database")
        return None


# Lấy dữ liệu từ bảng sinhvien
def get_students():
    conn = connect_db2()
    if conn:
        sql = "SELECT * FROM sinhvien"
        stmt = ibm_db.exec_immediate(conn, sql)
        students = []
        row = ibm_db.fetch_assoc(stmt)
        while row:
            students.append(row)
            row = ibm_db.fetch_assoc(stmt)
        return students
    return []


# API hiển thị trang web và dữ liệu
@app.route('/')
def home():
    students = get_students()
    print(students)
    return render_template('index4.html', students=students)


# API để thêm sinh viên
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    birthdate = request.form['birthdate']
    student_id = request.form['student_id']
    major = request.form['major']

    conn = connect_db2()
    if conn:
        sql = f"INSERT INTO sinhvien VALUES ('{name}', '{birthdate}', '{student_id}', '{major}')"
        ibm_db.exec_immediate(conn, sql)
    return redirect(url_for('home'))


# API để xóa sinh viên
@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    conn = connect_db2()
    if conn:
        sql = f"""DELETE FROM sinhvien WHERE "Mã Số" = '{student_id}'"""
        print(sql)
        ibm_db.exec_immediate(conn, sql)
    return redirect(url_for('home'))


if __name__ == '__main__':

    app.run(port=5000)
