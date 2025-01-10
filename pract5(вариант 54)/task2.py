import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['DB']  
collection = db['test2']  

with open('task_2_item.text', 'r', encoding='utf-8') as file:
    content = file.read().strip().split('=====')
    data = []
    for item in content:
        if item.strip():
            record = {}
            for line in item.strip().split('\n'):
                key, value = line.split('::')
                record[key.strip()] = value.strip()
            # Преобразуем типы данных
            record['salary'] = int(record['salary'])
            record['id'] = int(record['id'])
            record['year'] = int(record['year'])
            record['age'] = int(record['age'])
            data.append(record)
    collection.insert_many(data)

salary_stats = collection.aggregate([
    {
        '$group': {
            '_id': None,
            'min_salary': {'$min': '$salary'},
            'avg_salary': {'$avg': '$salary'},
            'max_salary': {'$max': '$salary'}
        }
    }
])
salary_stats = list(salary_stats)[0]
print(f"Минимальная зарплата: {salary_stats['min_salary']}, Средняя зарплата: {salary_stats['avg_salary']}, Максимальная зарплата: {salary_stats['max_salary']}")

job_count = collection.aggregate([
    {
        '$group': {
            '_id': '$job',
            'count': {'$sum': 1}
        }
    }
])
print("Количество данных по профессиям:")
for job in job_count:
    print(f"{job['_id']}: {job['count']}")

city_salary_stats = collection.aggregate([
    {
        '$group': {
            '_id': '$city',
            'min_salary': {'$min': '$salary'},
            'avg_salary': {'$avg': '$salary'},
            'max_salary': {'$max': '$salary'}
        }
    }
])
print("Минимальная, средняя, максимальная зарплата по городам:")
for city in city_salary_stats:
    print(f"{city['_id']}: Минимальная: {city['min_salary']}, Средняя: {city['avg_salary']}, Максимальная: {city['max_salary']}")

job_salary_stats = collection.aggregate([
    {
        '$group': {
            '_id': '$job',
            'min_salary': {'$min': '$salary'},
            'avg_salary': {'$avg': '$salary'},
            'max_salary': {'$max': '$salary'}
        }
    }
])
print("Минимальная, средняя, максимальная зарплата по профессиям:")
for job in job_salary_stats:
    print(f"{job['_id']}: Минимальная: {job['min_salary']}, Средняя: {job['avg_salary']}, Максимальная: {job['max_salary']}")

city_age_stats = collection.aggregate([
    {
        '$group': {
            '_id': '$city',
            'min_age': {'$min': '$age'},
            'avg_age': {'$avg': '$age'},
            'max_age': {'$max': '$age'}
        }
    }
])
print("Минимальный, средний, максимальный возраст по городам:")
for city in city_age_stats:
    print(f"{city['_id']}: Минимальный: {city['min_age']}, Средний: {city['avg_age']}, Максимальный: {city['max_age']}")

job_age_stats = collection.aggregate([
    {
        '$group': {
            '_id': '$job',
            'min_age': {'$min': '$age'},
            'avg_age': {'$avg': '$age'},
            'max_age': {'$max': '$age'}
        }
    }
])
print("Минимальный, средний, максимальный возраст по профессиям:")
for job in job_age_stats:
    print(f"{job['_id']}: Минимальный: {job['min_age']}, Средний: {job['avg_age']}, Максимальный: {job['max_age']}")

max_salary_min_age = collection.aggregate([
    {
        '$group': {
            '_id': '$age',
            'max_salary': {'$max': '$salary'}
        }
    },
    {
        '$sort': {'_id': 1}
    }
])
min_age = None
max_salary = None
for record in max_salary_min_age:
    if min_age is None or record['_id'] < min_age:
        min_age = record['_id']
        max_salary = record['max_salary']
print(f"Максимальная зарплата при минимальном возрасте {min_age}: {max_salary}")

min_salary_max_age = collection.aggregate([
    {
        '$group': {
            '_id': '$age',
            'min_salary': {'$min': '$salary'}
        }
    },
    {
        '$sort': {'_id': -1}
    }
])
max_age = None
min_salary = None
for record in min_salary_max_age:
    if max_age is None or record['_id'] > max_age:
        max_age = record['_id']
        min_salary = record['min_salary']
print(f"Минимальная зарплата при максимальном возрасте {max_age}: {min_salary}")

city_age_high_salary = collection.aggregate([
    {
        '$match': {'salary': {'$gt': 50000}}
    },
    {
        '$group': {
            '_id': '$city',
            'min_age': {'$min': '$age'},
            'avg_age': {'$avg': '$age'},
            'max_age': {'$max': '$age'}
        }
    },
    {
        '$sort': {'avg_age': -1}
    }
])
print("Минимальный, средний, максимальный возраст по городам при зарплате > 50,000:")
for city in city_age_high_salary:
    print(f"{city['_id']}: Минимальный: {city['min_age']}, Средний: {city['avg_age']}, Максимальный: {city['max_age']}")

age_salary_range = collection.aggregate([
    {
        '$match': {
            'age': {'$gt': 18, '$lt': 25},
            'salary': {'$gt': 50, '$lt': 65}
        }
    },
    {
        '$group': {
            '_id': None,
            'min_salary': {'$min': '$salary'},
            'avg_salary': {'$avg': '$salary'},
            'max_salary': {'$max': '$salary'}
        }
    }
])
age_salary_range_stats = list(age_salary_range)[0]
print(f"Минимальная зарплата: {age_salary_range_stats['min_salary']}, Средняя зарплата: {age_salary_range_stats['avg_salary']}, Максимальная зарплата: {age_salary_range_stats['max_salary']}")

custom_query = collection.aggregate([
    {
        '$match': {
            'city': 'Сеговия', 
            'job': 'Водитель'
        }
    },
    {
        '$group': {
            '_id': '$job',
            'avg_salary': {'$avg': '$salary'},
            'count': {'$sum': 1}
        }
    },
    {
        '$sort': {'avg_salary': -1}
    }
])
print("Произвольный запрос с $match, $group, $sort:")
for record in custom_query:
    print(f"Профессия: {record['_id']}, Средняя зарплата: {record['avg_salary']}, Количество: {record['count']}")
