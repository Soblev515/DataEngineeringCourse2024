import pandas as pd
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore'] 
books_collection = db['books'] 
authors_collection = db['authors'] 

books_df = pd.read_csv('books.csv')
books_collection.insert_many(books_df.to_dict('records'))

with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)
    authors_collection.insert_many(authors_data)

high_rated_books = list(books_collection.find({'rating': {'$gt': 4.5}}))
print(f"Книги с рейтингом выше 4.5: {json.dumps(high_rated_books, indent=4)}")

recent_books = list(books_collection.find({'published_year': {'$gt': 1950}}))
print(f"Книги, опубликованные после 1950 года: {json.dumps(recent_books, indent=4)}")

fiction_books = list(books_collection.find({'genre': 'Fiction'}))
print(f"Книги жанра 'Fiction': {json.dumps(fiction_books, indent=4)}")

american_authors = list(authors_collection.find({'nationality': 'American'}, {'id': 1}))
american_books = list(books_collection.find({'author_id': {'$in': [author['id'] for author in american_authors]}}))
print(f"Книги, написанные американскими авторами: {json.dumps(american_books, indent=4)}")

orwell_books = list(books_collection.find({'author_id': 3}))
print(f"Книги, написанные Джорджем Оруэллом: {json.dumps(orwell_books, indent=4)}")

genre_count = list(books_collection.aggregate([
    {'$group': {'_id': '$genre', 'count': {'$sum': 1}}}
]))
print(f"Количество книг по жанрам: {json.dumps(genre_count, indent=4)}")

avg_rating_by_author = list(books_collection.aggregate([
    {'$group': {'_id': '$author_id', 'average_rating': {'$avg': '$rating'}}},
    {'$lookup': {
        'from': 'authors',
        'localField': '_id',
        'foreignField': 'id',
        'as': 'author_info'
    }},
    {'$unwind': '$author_info'},
    {'$project': {'author': '$author_info.name', 'average_rating': 1}}
]))
print(f"Средний рейтинг книг по авторам: {json.dumps(avg_rating_by_author, indent=4)}")

max_rating_books = list(books_collection.aggregate([
    {'$group': {'_id': '$genre', 'max_rating': {'$max': '$rating'}}},
    {'$lookup': {
        'from': 'books',
        'let': {'max_rating': '$max_rating', 'genre': '$_id'},
        'pipeline': [
            {'$match': {'$expr': {'$and': [
                {'$eq': ['$rating', '$$max_rating']},
                {'$eq': ['$genre', '$$genre']}
            ]}}},
            {'$project': {'title': 1, 'author_id': 1}}
        ],
        'as': 'highest_rated_books'
    }}
]))
print(f"Книги с максимальным рейтингом в каждом жанре: {json.dumps(max_rating_books, indent=4)}")

books_before_2000 = list(books_collection.aggregate([
    {'$match': {'published_year': {'$lt': 2000}}},
    {'$group': {'_id': '$author_id', 'count': {'$sum': 1}}}
]))
print(f"Количество книг, опубликованных до 2000 года, по авторам: {json.dumps(books_before_2000, indent=4)}")

authors_with_multiple_books = list(books_collection.aggregate([
    {'$group': {'_id': '$author_id', 'book_count': {'$sum': 1}}},
    {'$match': {'book_count': {'$gt': 2}}},
    {'$lookup': {
        'from': 'authors',
        'localField': '_id',
        'foreignField': 'id',
        'as': 'author_info'
    }},
    {'$unwind': '$author_info'},
    {'$project': {'author': '$author_info.name', 'book_count': 1}}
]))
print(f"Авторы с количеством книг больше 2: {json.dumps(authors_with_multiple_books, indent=4)}")

books_collection.update_one({'title': '1984'}, {'$inc': {'rating': 0.1}})
print("Рейтинг книги '1984' обновлен на 0.1.")

books_collection.delete_many({'rating': {'$lt': 4.0}})
print("Книги с рейтингом ниже 4.0 удалены.")

books_collection.update_many({'author_id': 3}, {'$set': {'published_year': 1950}})
print("Год публикации всех книг Джорджа Оруэлла обновлен на 1950.")

authors_with_books = list(books_collection.aggregate([
    {'$group': {'_id': '$author_id'}},
    {'$project': {'author_id': '$_id'}}
]))
authors_with_books_ids = [author['author_id'] for author in authors_with_books]
authors_collection.delete_many({'id': {'$nin': authors_with_books_ids}})
print("Авторы без книг удалены.")

authors_collection.update_one({'id': 9}, {'$set': {'nationality': 'Portuguese'}})
print("Национальность Пауло Коэльо обновлена на 'Portuguese'.")
