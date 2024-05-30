import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
db = sqlite3.connect('krc.db')

cursor = db.cursor()

create_table_sql = """
ALTER TABLE management
ADD COLUMN department TEXT CHECK (department IN ('Administration', 'IT', 'Writing', 'Editing', 'Finance', 'SMM'));

"""



cursor.execute(create_table_sql)

db.commit()
db.close