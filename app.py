from functools import wraps
from flask import Flask, render_template, request, send_file, url_for, redirect, session, jsonify
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import os
import io

app = Flask(__name__)
app.secret_key = 'dev'

# ADMIN PAGE SET UP ----------------------------------------------------------
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_function

# ADMIN LOGIN PAGES
@app.route('/a-admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        db = sqlite3.connect('krc.db')
        p = request.form.get("pass")
        cursor = db.execute("SELECT * FROM Admin WHERE name = ?", (request.form.get('username'),))
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

# MAIN ADMIN DASHBOARD
@app.route('/dash')
@login_required
def dashboard():
    return render_template('dashboard.html')
        
# TABLE OF ADMINS
@app.route('/admins', methods=['GET', 'POST'])
@login_required
def admins():
    db = sqlite3.connect('krc.db')
    cursor = db.cursor()
    cursor.execute("SELECT admin_id, name FROM Admin")
    admins = cursor.fetchall()
    db.close()
    return render_template('admin_tb.html', admins=admins)

# Route to handle admin deletion
@app.route('/delete_admin/<int:admin_id>', methods=['DELETE'])
@login_required
def delete_admin(admin_id):
    db = sqlite3.connect('krc.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM Admin WHERE admin_id = ?", (admin_id,))
    db.commit()
    db.close()
    return jsonify({'success': True}), 200

# UPLOAD NEW ADMIN
@app.route('/a-upload', methods=['GET', 'POST'])
@login_required
def aUpload():
    if request.method == 'POST':
        db = sqlite3.connect('krc.db')
        p = request.form.get("pass")
        cursor = db.execute("SELECT * FROM Admin WHERE name = ?", (request.form.get('username'),))
        rows = cursor.fetchall()
        # check if admin already exists
        if len(rows) == 1:
            error = 'admin already exists'
            db.close()
            return render_template('error.html', error=error)
        
        # insert admin into db
        p_hash = generate_password_hash(p)
        db.execute("INSERT INTO admin (name, password) VALUES (?, ?);", (request.form.get('username'), p_hash))
        db.commit()

        db.close()
        return redirect(url_for('admins'))
    else:
        return render_template("Uadmin.html")


# ERROR 
@app.route('/error')
@login_required
def error():
    return render_template('error.html')

# JOURNAL UPLOAD
@app.route('/j-upload', methods=['GET', 'POST'])
@login_required
def jUpload():
    if request.method == 'POST':
        db = sqlite3.connect('krc.db')
        cursor = db.cursor()

        # get data from html form
        issue = request.form.get('issue')
        volume = request.form.get('volume')
        date = request.form.get('date')
        pdf = request.files.get('j-pdf')

        # upload journal to db
        pdf_data = pdf.read()
        cursor.execute("INSERT INTO Journals (issue, volume, date, pdf) VALUES (?, ?, ?, ?)", (issue, volume, date, pdf_data))
        db.commit()
        db.close()

        return redirect(url_for("journals"))
    else:
        return render_template("j-upload.html")

# TABLE OF JOURNALS
@app.route('/journals', methods=['GET'])
@login_required
def journals():
    db = sqlite3.connect('krc.db')
    cursor = db.cursor()
    cursor.execute("SELECT journal_id, issue, volume, date FROM Journals")
    journals = cursor.fetchall()
    db.close()
    return render_template("journal-tb.html", journals=journals)

# Route to handle journal deletion
@app.route('/delete_journal/<int:journal_id>', methods=['DELETE'])
@login_required
def delete_journal(journal_id):
    db = sqlite3.connect('krc.db')
    cursor = db.cursor()
    cursor.execute("DELETE FROM Journals WHERE journal_id = ?", (journal_id,))
    db.commit()
    db.close()
    return jsonify({'success': True}), 200

# Route for downloading journal
@app.route('/download/<int:journal_id>', methods=['GET'])
@login_required
def download_journal(journal_id):
    db = sqlite3.connect('krc.db')
    cursor = db.cursor()
    cursor.execute("SELECT pdf FROM Journals WHERE journal_id = ?", (journal_id,))
    pdf_data = cursor.fetchone()[0]
    db.close()

    return send_file(
        io.BytesIO(pdf_data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'journal_{journal_id}.pdf'
    )
# -----------------------------------------------------------------------------


# SET UP VIEW FOR EACH NON ADMIN HTML PAGE  
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@app.route('/editors', methods=['GET', 'POST'])
def editor():
    return render_template("editor.html")


@app.route('/finance', methods=['GET', 'POST'])
def finance():
    return render_template("finance.html")

@app.route('/j-download', methods=['GET', 'POST'])
def jdownload():
    return render_template("j-download.html")

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    return render_template("journal.html")

@app.route('/organization', methods=['GET', 'POST'])
def organization():
    return render_template("organization.html")

@app.route('/people-behind', methods=['GET', 'POST'])
def pplbehind():
    return render_template("pplbehind.html")

@app.route('/smm', methods=['GET', 'POST'])
def smm():
    return render_template("smm.html")

@app.route('/writers', methods=['GET', 'POST'])
def writers():
    return render_template("writers.html")



if __name__=='__main__':
    app.run(debug=True)


