from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/create_db')
def create_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Create your tables and define their schema here
    # For example:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

    return 'Database created successfully!'

if __name__ == '__main__':
    app.run(debug=True)
