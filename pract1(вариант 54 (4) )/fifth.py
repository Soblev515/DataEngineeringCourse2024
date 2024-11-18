from bs4 import BeautifulSoup
import csv
import re
input_file = "fifth_task.html"
output_file = "fifth_task_out.csv"
with open(input_file, 'r', encoding='utf-8') as f:
    html_content = f.read()
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
data = []
for row in rows:
    cols = row.find_all(['td', 'th'])
    row_data = [col.text.strip() for col in cols]
    if row_data[0] == "54":
        data.append(row_data)
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)
