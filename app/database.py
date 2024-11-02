import sqlite3

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database
def initialize_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            threshold INTEGER NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def get_items():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM inventory').fetchall()
    
    # Assuming the inventory table has item_name, quantity, and threshold columns
    items = [
        {
            "item_name": row['item_name'],
            "quantity": row['quantity'],
            "threshold": row['threshold']
        }
        for row in rows
    ]
    
    conn.close()
    return items


def add_item(item_name, quantity, threshold):
    conn = get_db_connection()
    conn.execute('INSERT INTO inventory (item_name, quantity, threshold) VALUES (?, ?, ?)', 
                 (item_name, quantity, threshold))
    conn.commit()
    conn.close()

def update_item(item_id, item_name, quantity, threshold):
    conn = get_db_connection()
    conn.execute('UPDATE inventory SET item_name = ?, quantity = ?, threshold = ? WHERE id = ?', 
                 (item_name, quantity, threshold, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
