import sqlite3
import pandas as pd
import msgpack
import msgpack_numpy as m

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY,
    name TEXT,
    street TEXT,
    city TEXT,
    zipcode INTEGER,
    floors INTEGER,
    year INTEGER,
    parking BOOLEAN,
    prob_price REAL,
    views INTEGER
)
''')

with open('item.msgpack', 'rb') as f:
    unpacked_data = msgpack.unpack(f, object_hook=m.decode)

properties_data = pd.DataFrame(unpacked_data)
properties_data.to_sql('properties', conn, if_exists='append', index=False)

VAR = 54

query1 = f'''
SELECT * FROM properties
ORDER BY prob_price
LIMIT {VAR + 10}
'''
result1 = pd.read_sql_query(query1, conn)
result1.to_json('out1.json', orient='records', lines=True)

query2 = '''
SELECT 
    SUM(prob_price) AS total,
    MIN(prob_price) AS min,
    MAX(prob_price) AS max,
    AVG(prob_price) AS average
FROM properties
'''
result2 = pd.read_sql_query(query2, conn)
print(f"Сумма: {result2['total'].values[0]}, Мин: {result2['min'].values[0]}, Макс: {result2['max'].values[0]}, Среднее: {result2['average'].values[0]}")

query3 = '''
SELECT city, COUNT(*) AS frequency
FROM properties
GROUP BY city
'''
result3 = pd.read_sql_query(query3, conn)
print(f"Частота встречаемости для категориального поля city:\n{result3}")

query4 = f'''
SELECT * FROM properties
WHERE parking = 1
ORDER BY prob_price
LIMIT {VAR + 10}
'''
result4 = pd.read_sql_query(query4, conn)
result4.to_json('out4.json', orient='records', lines=True)

conn.commit()
conn.close()
