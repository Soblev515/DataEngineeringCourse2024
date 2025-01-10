import sqlite3
import pandas as pd

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    quantity INTEGER,
    fromCity TEXT,
    isAvailable BOOLEAN,
    views INTEGER,
    update_count INTEGER DEFAULT 0
)
''')

product_data = pd.read_csv('_product_data.csv', sep=';', on_bad_lines='skip')
product_data.to_sql('products', conn, if_exists='append', index=False)

update_data = pd.read_pickle('_update_data.pkl')
conn.execute('BEGIN TRANSACTION')

try:
    for index, row in update_data.iterrows():
        product_name = row['name']
        command = row['command']
        
        if command == 'update_price':
            new_price = row['new_price']
            cursor.execute('''
                UPDATE products
                SET price = ?, update_count = update_count + 1
                WHERE name = ? AND price >= 0
            ''', (new_price, product_name))
        
        elif command == 'update_quantity':
            new_quantity = row['new_quantity']
            if new_quantity < 0:
                raise ValueError("Quantity cannot be negative")
            cursor.execute('''
                UPDATE products
                SET quantity = ?, update_count = update_count + 1
                WHERE name = ?
            ''', (new_quantity, product_name))
        
        elif command == 'remove':
            cursor.execute('''
                DELETE FROM products
                WHERE name = ?
            ''', (product_name,))
        
        elif command == 'return_sale':
            quantity_returned = row['quantity_returned']
            cursor.execute('''
                UPDATE products
                SET quantity = quantity + ?, update_count = update_count + 1
                WHERE name = ?
            ''', (quantity_returned, product_name))

    conn.commit()

except Exception as e:
    print(f"Error occurred: {e}")
    conn.rollback()

top_updated_products = pd.read_sql_query('''
    SELECT name, update_count
    FROM products
    ORDER BY update_count DESC
    LIMIT 10
''', conn)

print(f"Топ-10 самых обновляемых товаров:\n{top_updated_products}")

price_analysis = pd.read_sql_query('''
    SELECT 
        COUNT(*) AS count,
        SUM(price) AS total,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        AVG(price) AS avg_price
    FROM products
    GROUP BY isAvailable
''', conn)

print(f"\nАнализ цен товаров:\n{price_analysis}")

quantity_analysis = pd.read_sql_query('''
    SELECT 
        COUNT(*) AS count,
        SUM(quantity) AS total,
        MIN(quantity) AS min_quantity,
        MAX(quantity) AS max_quantity,
        AVG(quantity) AS avg_quantity
    FROM products
    GROUP BY isAvailable
''', conn)

print(f"\nАнализ остатков товаров:\n{quantity_analysis}")

available_products = pd.read_sql_query('''
    SELECT * FROM products
    WHERE isAvailable = 1
''', conn)

print(f"\nДоступные товары:\n{available_products}")

conn.close()
