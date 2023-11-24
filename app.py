from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

# Endpoint untuk mendapatkan data semua mahasiswa
@app.route('/students', methods=['POST'])
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    students_list = []
    for student in data:
        student_dict = {
            'id': student[0],
            'name': student[1],
            'email': student[2],
            'phone': student[3]
        }
        students_list.append(student_dict)
    return jsonify({'students': students_list})

# Endpoint untuk mendapatkan data semua mahasiswa
@app.route('/students/details/<int:id>', methods=['POST'])
def detail_students(id):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM students
        WHERE id=%s
        """, (id,))

    data = cur.fetchall()
    cur.close()

    if not data:
        return jsonify({'message': 'Mahasiswa tidak ditemukan'}), 404

    students_list = []
    for student in data:
        student_dict = {
            'id': student[0],
            'name': student[1],
            'email': student[2],
            'phone': student[3]
        }
        students_list.append(student_dict)

    return jsonify({'students': students_list})

# Endpoint untuk menambahkan data mahasiswa
@app.route('/students/create', methods=['POST'])
def create_student():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data Inserted Successfully'})

# Endpoint untuk menghapus data mahasiswa berdasarkan ID
@app.route('/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Record Has Been Deleted Successfully'})

# Endpoint untuk memperbarui data mahasiswa
@app.route('/students/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE students SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data Updated Successfully'})

if __name__ == "__main__":
    app.run(debug=True)

    