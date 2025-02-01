from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    conn = sqlite3.connect('C:/Users/user/Desktop/test.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ? AND role = ?',
                        (username, password, 'admin')).fetchone()
    conn.close()
    if user:
        session['user_id'] = user['id']
        session['role'] = user['role']
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/user_login')
def user_login():
    session['role'] = 'user'
    return redirect(url_for('user'))

@app.route('/admin')
def admin():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    organizations = conn.execute('SELECT * FROM organizations').fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    actions = conn.execute('SELECT * FROM actions').fetchall()
    conn.close()
    return render_template('admin.html', patients=patients, organizations=organizations, categories=categories, actions=actions)

@app.route('/user')
def user():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    organizations = conn.execute('SELECT * FROM organizations').fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    actions = conn.execute('SELECT * FROM actions').fetchall()
    observations = conn.execute('SELECT * FROM observations').fetchall()
    completed_observations = conn.execute('SELECT * FROM completed_observations').fetchall()
    conn.close()
    return render_template('user.html', patients=patients, organizations=organizations, categories=categories, actions=actions, observations=observations, completed_observations=completed_observations)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/add_patient', methods=['POST'])
def add_patient():
    conn = get_db_connection()
    conn.execute('INSERT INTO patients (name) VALUES (?)', ('Пациент ' + str(len(conn.execute('SELECT * FROM patients').fetchall()) + 1),))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/add_organization', methods=['POST'])
def add_organization():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO organizations (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/add_action', methods=['POST'])
def add_action():
    category_id = request.form['category_id']
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO actions (category_id, name) VALUES (?, ?)', (category_id, name))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/start_observation', methods=['POST'])
def start_observation():
    patient_id = request.form['patient_id']
    position = request.form['position']
    organization_id = request.form['organization_id']
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    conn.execute('INSERT INTO observations (patient_id, position, organization_id, start_time) VALUES (?, ?, ?, ?)',
                 (patient_id, position, organization_id, start_time))
    conn.commit()
    conn.close()
    return redirect(url_for('user'))

@app.route('/end_observation', methods=['POST'])
def end_observation():
    observation_id = request.form['observation_id']
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    observation = conn.execute('SELECT * FROM observations WHERE id = ?', (observation_id,)).fetchone()
    start_time = datetime.strptime(observation['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    duration = (end_time - start_time).seconds
    conn.execute('UPDATE observations SET end_time = ?, duration = ? WHERE id = ?', (end_time, duration, observation_id))
    conn.execute('INSERT INTO completed_observations (patient_id, position, organization_id, start_time, end_time, total_time) VALUES (?, ?, ?, ?, ?, ?)',
                 (observation['patient_id'], observation['position'], observation['organization_id'], observation['start_time'], end_time, duration))
    conn.commit()
    conn.close()
    return redirect(url_for('user'))

if __name__ == '__main__':
    app.run(debug=True)
