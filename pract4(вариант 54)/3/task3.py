import sqlite3
import pandas as pd

VAR = 54

conn = sqlite3.connect('music.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS music_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT,
    song TEXT,
    duration_ms INTEGER,
    year INTEGER,
    tempo REAL,
    genre TEXT,
    instrumentalness REAL,
    explicit BOOLEAN,
    loudness REAL
)
''')

part1_data = pd.read_csv('_part_1.csv', sep=';')

part2_data = []
with open('_part_2.text', 'r', encoding='utf-8') as file:
    entry = {}
    for line in file:
        line = line.strip()
        if line == '=====':
            if entry:
                part2_data.append(entry)
                entry = {}
        else:
            key, value = line.split('::')
            entry[key] = value

part2_df = pd.DataFrame(part2_data)
part2_df['duration_ms'] = part2_df['duration_ms'].astype(int)
part2_df['year'] = part2_df['year'].astype(int)
part2_df['tempo'] = part2_df['tempo'].astype(float)
part2_df['instrumentalness'] = part2_df['instrumentalness'].astype(float)
part2_df['explicit'] = part2_df['explicit'].map({'True': True, 'False': False})
part2_df['loudness'] = part2_df['loudness'].astype(float)

# Проверка и удаление колонок 'energy' и 'key', если они существуют
for column in ['energy', 'key']:
    if column in part1_data.columns:
        part1_data = part1_data.drop(columns=[column])
    if column in part2_df.columns:
        part2_df = part2_df.drop(columns=[column])

combined_data = pd.concat([part1_data, part2_df], ignore_index=True)

# Проверка колонок перед вставкой
print(combined_data.columns)

combined_data.to_sql('music_data', conn, if_exists='append', index=False)

query1 = f'''
SELECT * FROM music_data
ORDER BY duration_ms
LIMIT {VAR + 10}
'''
result1 = pd.read_sql_query(query1, conn)
result1.to_json('out1.json', orient='records', lines=True)

query2 = '''
SELECT 
    SUM(duration_ms) AS total_duration,
    MIN(duration_ms) AS min_duration,
    MAX(duration_ms) AS max_duration,
    AVG(duration_ms) AS avg_duration
FROM music_data
'''
result2 = pd.read_sql_query(query2, conn)
print(f"Сумма: {result2['total_duration'].values[0]}, Мин: {result2['min_duration'].values[0]}, Макс: {result2['max_duration'].values[0]}, Среднее: {result2['avg_duration'].values[0]}")

query3 = '''
SELECT genre, COUNT(*) AS frequency
FROM music_data
GROUP BY genre
'''
result3 = pd.read_sql_query(query3, conn)
print(f"Частота встречаемости для жанра:\n{result3}")

query4 = f'''
SELECT * FROM music_data
WHERE explicit = 1
ORDER BY duration_ms
LIMIT {VAR + 15}
'''
result4 = pd.read_sql_query(query4, conn)
result4.to_json('out4.json', orient='records', lines=True)

conn.commit()
conn.close()
