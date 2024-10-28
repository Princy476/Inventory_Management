import sqlite3

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('inventory.db')  # Creates 'inventory.db' in the current folder if not present
    conn.row_factory = sqlite3.Row  # This will return rows as dictionaries
    return conn

# Function to initialize the database
def initialize_db():
    conn = get_db_connection()
    # Create table if it doesn't exist
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
    items = conn.execute('SELECT * FROM inventory').fetchall()
    conn.close()
    return items

def add_item(item_name, quantity, threshold):
    conn = get_db_connection()
    conn.execute('INSERT INTO inventory (item_name, quantity, threshold) VALUES (?, ?, ?)', 
                 (item_name, quantity, threshold))
    conn.commit()
    conn.close()

def update_item(item_id, quantity, threshold):
    # Update item logic
    pass

def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
