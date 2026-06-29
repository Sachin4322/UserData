from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root123"),
        database=os.getenv("MYSQL_DATABASE", "membersdb")
    )

# Wait for MySQL startup
time.sleep(10)

@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            gender VARCHAR(20),
            mobile VARCHAR(20),
            age INT
        )
    """)

    # Fetch all members
    cursor.execute("SELECT * FROM members ORDER BY id DESC")
    members = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", members=members)


@app.route('/save', methods=['POST'])
def save():
    db = get_db()
    cursor = db.cursor()

    name = request.form['name']
    gender = request.form['gender']
    mobile = request.form['mobile']
    age = request.form['age']

    cursor.execute(
        "INSERT INTO members(name, gender, mobile, age) VALUES (%s, %s, %s, %s)",
        (name, gender, mobile, age)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
