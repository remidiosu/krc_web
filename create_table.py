import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
db = sqlite3.connect('krc.db')

cursor = db.cursor()
db.commit()
db.close