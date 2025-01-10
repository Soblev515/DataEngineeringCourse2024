import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['DB'] 
collection = db['task3'] 

with open('task_3_item.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    collection.insert_many(data)

# 1. Удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
collection.delete_many({'$or': [{'salary': {'$lt': 25000}}, {'salary': {'$gt': 175000}}]})
print("Документы с зарплатой < 25000 или > 175000 удалены.")

# 2. Увеличить возраст (age) всех документов на 1
collection.update_many({}, {'$inc': {'age': 1}})
print("Возраст всех документов увеличен на 1.")

# 3. Поднять заработную плату на 5% для произвольно выбранных профессий
selected_professions = ['Учитель', 'Повар'] 
collection.update_many({'job': {'$in': selected_professions}}, {'$mul': {'salary': 1.05}})
print("Заработная плата на 5% повышена для выбранных профессий.")

# 4. Поднять заработную плату на 7% для произвольно выбранных городов
selected_cities = ['Мадрид', 'Осера'] 
collection.update_many({'city': {'$in': selected_cities}}, {'$mul': {'salary': 1.07}})
print("Заработная плата на 7% повышена для выбранных городов.")

# 5. Поднять заработную плату на 10% для выборки по сложному предикату
complex_city = 'Эль-Пуэрто-де-Санта-Мария'  
complex_professions = ['Оператор call-центра']  
age_range = (20, 40) 
collection.update_many({
    'city': complex_city,
    'job': {'$in': complex_professions},
    'age': {'$gte': age_range[0], '$lte': age_range[1]}
}, {'$mul': {'salary': 1.10}})
print("Заработная плата на 10% повышена для сложного предиката.")

# 6. Удалить из коллекции записи по произвольному предикату
arbitrary_predicate = {'job': 'Повар'} 
collection.delete_many(arbitrary_predicate)
print("Записи по произвольному предикату удалены.")
