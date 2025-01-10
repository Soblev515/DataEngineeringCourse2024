import sqlite3
import pandas as pd

conn = sqlite3.connect('office_management.db')

# Загрузка данных сотрудников
employees_data = pd.read_csv('employees.csv')
employees_data.to_sql('employees', conn, if_exists='append', index=False)

# Загрузка данных проектов
projects_data = pd.read_csv('projects.csv')
projects_data.to_sql('projects', conn, if_exists='append', index=False)

# Загрузка данных задач
tasks_data = pd.read_csv('tasks.csv')
tasks_data.to_sql('tasks', conn, if_exists='append', index=False)

conn.commit()
conn.close()
