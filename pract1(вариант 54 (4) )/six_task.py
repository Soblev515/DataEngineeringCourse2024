import requests
import json
import html

api_url = "https://jsonplaceholder.typicode.com/todos"
output_file = "six_out.html"

response = requests.get(api_url)
response.raise_for_status()
data = response.json()

html_output = """
      <!DOCTYPE html>
      <html>
      <head>
          <title>API Data</title>
          <style>
              table {
                  width: 100%;
                  border-collapse: collapse;
              }
              th, td {
                  border: 1px solid black;
                  padding: 8px;
                  text-align: left;
              }
          </style>
      </head>
      <body>
          <h1>Данные из API</h1>
          <table>
              <tr>
                  <th>Название</th>
                  <th>Значение</th>
              </tr>
      """
for item in data:
        html_output += "<tr><td>" + html.escape(str(next(iter(item.keys())))) + "</td><td>" + html.escape(str(next(iter(item.values())))) + "</td></tr>"

html_output += """
          </table>
      </body>
      </html>
      """

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_output)
