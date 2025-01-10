import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Шаг 1: Загрузка набора данных из файла
file_path = 'Consumer_Complaints.csv'
data = pd.read_csv(file_path)

# Шаг 2: Анализ набора данных
# a. Объем памяти, который занимает файл на диске
file_size = os.path.getsize(file_path) / (1024 * 1024)  # в МБ
print(f"Объем файла на диске: {file_size:.2f} МБ")

# b. Объем памяти, который занимает набор данных при загрузке в память
memory_usage = data.memory_usage(deep=True).sum() / (1024 * 1024)  # в МБ
print(f"Объем памяти в памяти: {memory_usage:.2f} МБ")

# c. Вычисление объема памяти для каждой колонки
memory_info = data.memory_usage(deep=True).to_frame(name='Memory Usage (bytes)')
memory_info['Memory Usage (MB)'] = memory_info['Memory Usage (bytes)'] / (1024 * 1024)
memory_info['Percentage of Total Memory'] = (memory_info['Memory Usage (bytes)'] / memory_usage) * 100
memory_info['Data Type'] = data.dtypes

print(memory_info)

# Шаг 3: Сортировка по занимаемому объему памяти и сохранение в CSV
sorted_memory_info = memory_info.sort_values(by='Memory Usage (bytes)', ascending=False)
sorted_memory_info.to_csv('memory_usage_statistics.csv', index=True)

# Шаг 4: Преобразование колонок с типом данных «object» в категориальные
for col in data.select_dtypes(include=['object']):
    if data[col].nunique() / len(data) < 0.5:
        data[col] = data[col].astype('category')

# Шаг 5: Понижающее преобразование типов «int» колонок
for col in data.select_dtypes(include=['int']):
    data[col] = pd.to_numeric(data[col], downcast='integer')

# Шаг 6: Понижающее преобразование типов «float» колонок
for col in data.select_dtypes(include=['float']):
    data[col] = pd.to_numeric(data[col], downcast='float')

# Шаг 7: Повторный анализ набора данных
memory_usage_after = data.memory_usage(deep=True).sum() / (1024 * 1024)  # в МБ
print(f"Объем памяти после оптимизации: {memory_usage_after:.2f} МБ")

# Шаг 8: Выбор 10 колонок и сохранение поднабора
selected_columns = ['Date received', 'Product', 'Issue', 'Company', 'State', 'ZIP code', 'Consumer complaint narrative', 'Company response to consumer', 'Timely response?', 'Complaint ID']
data_subset = data[selected_columns]
data_subset.to_csv('Consumer_Complaints_subset.csv', index=False)

# Шаг 9: Построение графиков
# График 1: Количество жалоб по продуктам (столбчатый график)
plt.figure(figsize=(10, 6))
sns.countplot(y='Product', data=data_subset)
plt.title('Количество жалоб по продуктам')
plt.xlabel('Количество жалоб')
plt.ylabel('Продукты')
plt.savefig('product_complaints_count.png')
plt.clf()

# График 2: Топ-10 штатов с наибольшим количеством жалоб (столбчатый график)
plt.figure(figsize=(10, 6))
data_subset['State'].value_counts().head(10).plot(kind='bar')
plt.title('Топ-10 штатов с наибольшим количеством жалоб')
plt.xlabel('Штат')
plt.ylabel('Количество жалоб')
plt.xticks(rotation=45)
plt.savefig('top_states_complaints.png')
plt.clf()

# График 3: Распределение жалоб по продуктам в зависимости от своевременности ответа (столбчатый график)
plt.figure(figsize=(10, 6))
sns.countplot(x='Product', hue='Timely response?', data=data_subset)
plt.title('Распределение жалоб по продуктам в зависимости от своевременности ответа')
plt.xlabel('Продукты')
plt.ylabel('Количество жалоб')
plt.xticks(rotation=45)
plt.legend(title='Своевременный ответ?', loc='upper right')
plt.savefig('product_timely_response_distribution.png')
plt.clf()

# График 4: Количество жалоб по типам проблем (Issues) (столбчатый график)
plt.figure(figsize=(10, 6))
sns.countplot(y='Issue', data=data_subset)
plt.title('Количество жалоб по типам проблем')
plt.xlabel('Количество жалоб')
plt.ylabel('Типы проблем')
plt.savefig('issue_complaints_count.png')
plt.clf()

# График 5: Процент жалоб, на которые компании ответили вовремя (круговая диаграмма)
plt.figure(figsize=(8, 8))
data_subset['Timely response?'].value_counts(normalize=True).plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Процент жалоб с вовремя полученными ответами')
plt.ylabel('')
plt.savefig('timely_response_percentage.png')
plt.clf()

# График 6: Топ-10 компаний с наибольшим количеством жалоб (столбчатый график)
plt.figure(figsize=(10, 6))
data_subset['Company'].value_counts().head(10).plot(kind='bar')
plt.title('Топ-10 компаний с наибольшим количеством жалоб')
plt.xlabel('Компания')
plt.ylabel('Количество жалоб')
plt.xticks(rotation=45)
plt.savefig('top_companies_complaints.png')
plt.clf()


# График 7: Распределение жалоб по почтовым индексам (топ-20) (столбчатый график)
plt.figure(figsize=(10, 6))
data_subset['ZIP code'].value_counts().head(20).plot(kind='bar')
plt.title('Топ-20 почтовых индексов с наибольшим количеством жалоб')
plt.xlabel('Почтовый индекс')
plt.ylabel('Количество жалоб')
plt.xticks(rotation=45)
plt.savefig('top_zip_codes_complaints.png')
plt.clf()

