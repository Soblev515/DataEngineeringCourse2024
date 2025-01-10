import sqlite3
import json
import pandas as pd

conn = sqlite3.connect('office_management.db')

# Запрос 1: Выборка сотрудников, занимающих должность "Developer", с сортировкой по имени
query1 = '''
SELECT * FROM employees
WHERE position = 'Developer'
ORDER BY name
LIMIT 5
'''
developers = pd.read_sql_query(query1, conn)
developers.to_json('out1.json', orient='records', lines=True)

# Запрос 2: Подсчет количества задач по статусу
query2 = '''
SELECT status, COUNT(*) as count
FROM tasks
GROUP BY status
'''
task_counts = pd.read_sql_query(query2, conn)
task_counts.to_json('out2.json', orient='records', lines=True)

# Запрос 3: Получение всех проектов с количеством задач по каждому проекту
query3 = '''
SELECT p.name, COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id
'''
project_task_counts = pd.read_sql_query(query3, conn)
project_task_counts.to_json('out3.json', orient='records', lines=True)

# Запрос 4: Обновление статуса задачи
update_query = '''
UPDATE tasks
SET status = 'Completed'
WHERE id = 2
'''
conn.execute(update_query)
conn.commit()

# Запрос 5: Получение задач, назначенных на конкретного сотрудника
query5 = '''
SELECT t.description, t.status
FROM tasks t
JOIN employees e ON t.employee_id = e.id
WHERE e.name = 'John Doe'
'''
john_tasks = pd.read_sql_query(query5, conn)
john_tasks.to_json('out5.json', orient='records', lines=True)

conn.close()
