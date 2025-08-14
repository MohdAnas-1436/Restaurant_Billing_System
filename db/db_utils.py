import sqlite3
import pandas as pd
from datetime import datetime
import json

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    
    # Create menu table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            gst_rate REAL DEFAULT 5.0,
            available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            service_mode TEXT NOT NULL,
            customer_name TEXT,
            customer_phone TEXT,
            table_number TEXT,
            subtotal REAL NOT NULL,
            gst_amount REAL NOT NULL,
            discount_amount REAL DEFAULT 0,
            grand_total REAL NOT NULL,
            payment_method TEXT NOT NULL,
            order_status TEXT DEFAULT 'Completed',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            items_json TEXT NOT NULL
        )
    ''')
    
    # Create order_items table for detailed tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_menu_item(name, category, price, gst_rate=5.0):
    """Add a new item to the menu"""
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO menu (name, category, price, gst_rate)
        VALUES (?, ?, ?, ?)
    ''', (name, category, price, gst_rate))
    
    conn.commit()
    conn.close()

def get_menu_items():
    """Get all menu items"""
    conn = sqlite3.connect('db/restaurant.db')
    menu_df = pd.read_sql_query(
        "SELECT * FROM menu WHERE available = 1 ORDER BY category, name",
        conn
    )
    conn.close()
    return menu_df

def update_menu_item(item_id, name, category, price, gst_rate, available):
    """Update a menu item"""
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE menu 
        SET name = ?, category = ?, price = ?, gst_rate = ?, available = ?
        WHERE id = ?
    ''', (name, category, price, gst_rate, available, item_id))
    
    conn.commit()
    conn.close()

def delete_menu_item(item_id):
    """Delete a menu item"""
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM menu WHERE id = ?', (item_id,))
    
    conn.commit()
    conn.close()

def generate_order_number():
    """Generate a unique order number"""
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    return f"ORD{timestamp}"

def save_order(order_data, order_items):
    """Save a completed order to the database"""
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    
    # Insert order
    cursor.execute('''
        INSERT INTO orders (
            order_number, service_mode, customer_name, customer_phone, 
            table_number, subtotal, gst_amount, discount_amount, 
            grand_total, payment_method, items_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_data['order_number'], order_data['service_mode'],
        order_data.get('customer_name', ''), order_data.get('customer_phone', ''),
        order_data.get('table_number', ''), order_data['subtotal'],
        order_data['gst_amount'], order_data['discount_amount'],
        order_data['grand_total'], order_data['payment_method'],
        json.dumps(order_items)
    ))
    
    order_id = cursor.lastrowid
    
    # Insert order items
    for item in order_items:
        cursor.execute('''
            INSERT INTO order_items (
                order_id, item_name, category, quantity, unit_price, total_price
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            order_id, item['name'], item.get('category', ''),
            item['quantity'], item['price'], item['price'] * item['quantity']
        ))
    
    conn.commit()
    conn.close()
    
    return order_id

def get_orders(date_from=None, date_to=None):
    """Get orders within date range"""
    conn = sqlite3.connect('db/restaurant.db')
    
    query = "SELECT * FROM orders"
    params = []
    
    if date_from and date_to:
        query += " WHERE DATE(order_date) BETWEEN ? AND ?"
        params = [date_from, date_to]
    elif date_from:
        query += " WHERE DATE(order_date) >= ?"
        params = [date_from]
    elif date_to:
        query += " WHERE DATE(order_date) <= ?"
        params = [date_to]
    
    query += " ORDER BY order_date DESC"
    
    orders_df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return orders_df

def get_sales_summary(date_from, date_to):
    """Get sales summary for a date range"""
    conn = sqlite3.connect('db/restaurant.db')
    
    # Daily sales
    daily_sales = pd.read_sql_query('''
        SELECT 
            DATE(order_date) as date,
            COUNT(*) as total_orders,
            SUM(grand_total) as total_sales,
            AVG(grand_total) as avg_order_value
        FROM orders 
        WHERE DATE(order_date) BETWEEN ? AND ?
        GROUP BY DATE(order_date)
        ORDER BY date
    ''', conn, params=[date_from, date_to])
    
    # Most sold items
    most_sold = pd.read_sql_query('''
        SELECT 
            item_name,
            category,
            SUM(quantity) as total_quantity,
            SUM(total_price) as total_revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        WHERE DATE(o.order_date) BETWEEN ? AND ?
        GROUP BY item_name, category
        ORDER BY total_quantity DESC
        LIMIT 10
    ''', conn, params=[date_from, date_to])
    
    # Payment method breakdown
    payment_breakdown = pd.read_sql_query('''
        SELECT 
            payment_method,
            COUNT(*) as order_count,
            SUM(grand_total) as total_amount
        FROM orders 
        WHERE DATE(order_date) BETWEEN ? AND ?
        GROUP BY payment_method
    ''', conn, params=[date_from, date_to])
    
    conn.close()
    
    return daily_sales, most_sold, payment_breakdown

def add_sample_menu():
    """Add sample menu items for testing"""
    sample_items = [
        # Appetizers
        ("Paneer Tikka", "Appetizers", 180, 5.0),
        ("Chicken Wings", "Appetizers", 220, 5.0),
        ("Veg Spring Rolls", "Appetizers", 150, 5.0),
        ("Fish Fingers", "Appetizers", 200, 5.0),
        
        # Main Course
        ("Butter Chicken", "Main Course", 320, 5.0),
        ("Paneer Butter Masala", "Main Course", 280, 5.0),
        ("Biryani (Chicken)", "Main Course", 350, 5.0),
        ("Biryani (Veg)", "Main Course", 280, 5.0),
        ("Dal Makhani", "Main Course", 220, 5.0),
        ("Rogan Josh", "Main Course", 340, 5.0),
        
        # Bread & Rice
        ("Butter Naan", "Bread & Rice", 60, 5.0),
        ("Garlic Naan", "Bread & Rice", 80, 5.0),
        ("Basmati Rice", "Bread & Rice", 120, 5.0),
        ("Jeera Rice", "Bread & Rice", 140, 5.0),
        
        # Beverages
        ("Lassi (Sweet)", "Beverages", 80, 5.0),
        ("Fresh Lime Soda", "Beverages", 60, 5.0),
        ("Masala Chai", "Beverages", 40, 5.0),
        ("Cold Coffee", "Beverages", 100, 5.0),
        ("Mango Juice", "Beverages", 90, 5.0),
        
        # Desserts
        ("Gulab Jamun", "Desserts", 120, 5.0),
        ("Rasgulla", "Desserts", 100, 5.0),
        ("Ice Cream", "Desserts", 80, 5.0),
        ("Kulfi", "Desserts", 90, 5.0),
    ]
    
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    
    for name, category, price, gst_rate in sample_items:
        cursor.execute('''
            INSERT OR IGNORE INTO menu (name, category, price, gst_rate)
            VALUES (?, ?, ?, ?)
        ''', (name, category, price, gst_rate))
    
    conn.commit()
    conn.close()
