import csv
import json
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DB'] 
collection = db['task1']

with open('task_1_item.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    data = []
    for row in reader:
        row['salary'] = int(row['salary'])
        row['id'] = int(row['id'])
        row['year'] = int(row['year'])
        row['age'] = int(row['age'])
        data.append(row)
    collection.insert_many(data)

# Запросы
top_10_salary = list(collection.find().sort('salary', -1).limit(10))
print(f"Топ 10 по зарплате: {json.dumps(top_10_salary, indent=4)}")

young_top_salary = list(collection.find({'age': {'$lt': 30}}).sort('salary', -1).limit(15))
print(f"Записи с возрастом меньше 30 лет: {json.dumps(young_top_salary, indent=4)}")

cities = ['Вильнюс', 'Хельсинки', 'Астана'] 
professions = ['Архитектор', 'Повар', 'IT-специалист']
complex_filter = list(collection.find({'city': {'$in': cities}, 'job': {'$in': professions}}).sort('age', 1).limit(10))
print(f"Записи по городу и профессии: {json.dumps(complex_filter, indent=4)}")

count_filtered = collection.count_documents({
    'age': {'$gte': 18, '$lte': 60},  # Замените на нужный диапазон
    'year': {'$gte': 2006, '$lte': 2011},
    '$or': [
        {'salary': {'$gt': 50000, '$lte': 75000}},
        {'salary': {'$gt': 125000, '$lt': 150000}}
    ]
})
print(f'Количество записей: {count_filtered}')
