import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS subitems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rating REAL,
    convenience INTEGER,
    security INTEGER,
    functionality INTEGER,
    comment TEXT,
    property_id INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
''')

subitems_data = pd.read_csv('subitem.csv', sep=';')

subitems_data['property_id'] = subitems_data['name'].map(
    lambda x: cursor.execute('SELECT id FROM properties WHERE name = ?', (x,)).fetchone()[0] if cursor.execute('SELECT id FROM properties WHERE name = ?', (x,)).fetchone() else None
)

subitems_data.to_sql('subitems', conn, if_exists='append', index=False)

query1 = '''
SELECT s.*, p.name AS property_name
FROM subitems s
JOIN properties p ON s.property_id = p.id
'''
result1 = pd.read_sql_query(query1, conn)
print(f"Все данные из subitems с соответствующими свойствами:\n{result1}")

query2 = '''
SELECT p.name, AVG(s.rating) AS average_rating
FROM properties p
LEFT JOIN subitems s ON p.id = s.property_id
GROUP BY p.id
'''
result2 = pd.read_sql_query(query2, conn)
print(f"Средний рейтинг для каждого свойства:\n{result2}")

query3 = '''
SELECT s.*, p.name AS property_name
FROM subitems s
JOIN properties p ON s.property_id = p.id
WHERE s.convenience > 3
'''
result3 = pd.read_sql_query(query3, conn)
print(f"Все subitems с удобствами выше 3:\n{result3}")

conn.commit()
conn.close()
