from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'jnavi-secret-key'

# Load users
def load_users():
    if os.path.exists("users.json"):
        with open("users.json") as f:
            return json.load(f)
    return {}

# Load missions
def load_missions():
    if os.path.exists("missions.json"):
        with open("missions.json") as f:
            return json.load(f)
    return []

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    users = load_users()
    username = data['username']
    users[username] = {
        "password": data['password'],
        "level": data['level'],
        "name": data.get('name', ''),
        "hobby": data.get('hobby', ''),
        "education": data.get('education', '')
    }
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['level'] = users[username]['level']
            return redirect(url_for('dashboard'))
        return "Login gagal!"
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    missions = load_missions()
    return render_template('dashboard.html', user=session['user'], level=session['level'], missions=missions)

# Buat misi (UMKM only)
@app.route('/buat_misi', methods=['POST'])
def buat_misi():
    if 'user' not in session or session['level'] != 'UMKM':
        return "Unauthorized"
    missions = load_missions()
    new_mission = {
        "title": request.form['title'],
        "desc": request.form['desc'],
        "gaji": request.form['gaji'],
        "oleh": session['user']
    }
    missions.append(new_mission)
    with open("missions.json", "w") as f:
        json.dump(missions, f, indent=2)
    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
