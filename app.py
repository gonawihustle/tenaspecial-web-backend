import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows your Surge.sh website to connect freely

DB_FILE = "tenaspecial_web.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Specialists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specialists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialty TEXT,
            fee REAL,
            telegram_username TEXT
        )
    """)
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            download_link TEXT
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "Tenaspecial Web API is running!"})

# --- SPECIALIST ENDPOINTS ---
@app.route('/api/specialists', methods=['GET'])
def get_specialists():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty, fee, telegram_username FROM specialists")
    rows = cursor.fetchall()
    conn.close()
    
    data = [{"id": r[0], "name": r[1], "specialty": r[2], "fee": r[3], "telegram_username": r[4]} for r in rows]
    return jsonify(data)

@app.route('/api/admin/add_specialist', methods=['POST'])
def add_specialist():
    data = request.json or {}
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO specialists (name, specialty, fee, telegram_username) VALUES (?, ?, ?, ?)",
        (data.get('name'), data.get('specialty'), data.get('fee'), data.get('telegram_username'))
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Specialist added successfully!"})

# --- PRODUCT ENDPOINTS ---
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, download_link FROM products")
    rows = cursor.fetchall()
    conn.close()
    
    data = [{"id": r[0], "name": r[1], "price": r[2], "download_link": r[3]} for r in rows]
    return jsonify(data)

@app.route('/api/admin/add_product', methods=['POST'])
def add_product():
    data = request.json or {}
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, download_link) VALUES (?, ?, ?)",
        (data.get('name'), data.get('price'), data.get('download_link'))
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Product added successfully!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
