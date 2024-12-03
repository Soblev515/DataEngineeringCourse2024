import glob
import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def extract_value(soup, start_string, end_string=None):
    """Извлекает значение из тега, используя регулярные выражения."""
    el = soup.find("span", string=re.compile(f"^{start_string}"))
    if el:
        text = el.text.strip()
        if ":" in text:
            parts = text.split(":", 1)
            value = parts[1].strip()
            if value:
                try:
                    return int(value) if value.isdigit() else float(value)
                except ValueError:
                    return value
            else:
                return None  
        else:
            return None
    else:
        return None

def parse_html_files(directory, output_filename="output.json"):
    all_data = []
    for filename in glob.glob(os.path.join(directory, "*.html")):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                item_data = {
                    "city": extract_value(soup, "Город:"),
                    "building": extract_value(soup, "Строение:"),
                    "address": extract_value(soup, "Улица:", "Индекс:"),
                    "floors": int(extract_value(soup, "Этажи:") or 0),
                    "year": int(extract_value(soup, "Построено в") or 0),
                    "parking": extract_value(soup, "Парковка:"),
                    "rating": float(extract_value(soup, "Рейтинг:") or 0.0),
                    "views": int(extract_value(soup, "Просмотры:") or 0)
                }
                all_data.append(item_data)
        except Exception as e:
            print(f"Ошибка при обработке файла '{filename}': {e}")


    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)



def process_data(json_filename, output_dir="first_output"):
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{json_filename}' не найден.")
        return

    df = pd.DataFrame(data)

    sorted_df = df.sort_values('rating', ascending=False)
    sorted_df.to_json(os.path.join(output_dir, "sorted_data.json"), orient="records", indent=4)

    filtered_df = df[df['parking'] == "есть"]
    filtered_df.to_json(os.path.join(output_dir, "filtered_data.json"), orient="records", indent=4)

    stats = df['views'].agg(['sum', 'min', 'max', 'mean', 'std'])
    stats_dict = stats.to_dict()
    with open(os.path.join(output_dir, "stats.json"), 'w') as f:
        json.dump(stats_dict, f, indent=4)

    freq = df['city'].value_counts().to_dict()
    with open(os.path.join(output_dir, "frequencies.json"), 'w', encoding='utf-8') as f:
        json.dump(freq, f, indent=4, ensure_ascii=False)

html_files_directory = "1"  
output_json_file = "first_data.json"
os.makedirs("1_output", exist_ok=True)

parse_html_files(html_files_directory, output_json_file)
process_data(output_json_file, "1_output")
