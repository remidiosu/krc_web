from functools import wraps
from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'jnelvrjaegnprgnopiagnvoqi43ngoi3409249251490'


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("base.html")


@app.route('/remi', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        db = sqlite3.connect('krc.db')
        p = request.form.get("pass")
        cursor = db.execute("SELECT * FROM admin WHERE name = ?", (request.form.get('username'),))
        rows = cursor.fetchall()
        db.close()

        if (len(rows) == 1) and check_password_hash(rows[0][2], p):
            session['admin'] = 'admin'
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))
    else:
        return render_template('admin.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/dash', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
        

@app.route('/j-upload', methods=['GET', 'POST'])
@login_required
def jUpload():
    return render_template("j-upload.html")


@app.route('/m-upload', methods=['GET', 'POST'])
@login_required
def mUpload():
    return render_template("m-upload.html")


@app.route('/s-upload', methods=['GET', 'POST'])
@login_required
def sUpload():
    return render_template("s-upload.html")


@app.route('/a-upload', methods=['GET', 'POST'])
@login_required
def aUpload():
    return render_template("a-upload.html")

@app.route('/members', methods=['GET', 'POST'])
@login_required
def members():
    db = sqlite3.connect('krc.db')
    cursor = db.execute('SELECT * FROM management')
    rows = cursor.fetchall()
    db.close()
    if request.method == 'POST':
        db = sqlite3.connect('krc.db')
        id_to_delete = request.form.get('member_id')
        db.execute('DELETE FROM management WHERE id = ?', (id_to_delete,))
        db.close()
        return render_template('members.html')
    else:
        return render_template('members.html', rows=rows)


@app.route('/a-member', methods=['GET', 'POST'])
@login_required
def addmember():
    if request.method == 'POST':
        db = sqlite3.connect('krc.db')
        full_name = request.form.get('fname')
        role = request.form.get('role')
        email = request.form.get('email')
        joined_date = request.form.get('joined-date')
        photo = request.files.get('photo')
        
        cursor = db.execute("INSERT INTO management (name, role, email, joined_date, photo) VALUES (?, ?, ?, ?, ?)", (full_name, role, email, joined_date, photo))
        cursor.commit()
        db.close()

        return redirect('/')
    else:
        return render_template('add_member.html')



if __name__=='__main__':
    app.run(debug=True)


