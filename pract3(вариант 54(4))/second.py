import glob
import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def extract_data(soup):
    products = []
    for item in soup.find_all("div", class_="product-item"):
        product = {}
        product["id"] = item.find("a", class_="add-to-favorite")["data-id"]
        product["name"] = item.find("span").text.strip()
        product["price"] = int(item.find("price").text.strip().replace("₽", "").replace(" ", ""))
        for li in item.find("ul").find_all("li"):
            product[li["type"]] = li.text.strip()

        products.append(product)
    return products

def parse_html_files(directory, output_filename="output.json"):
    all_data = []
    for filename in glob.glob(os.path.join(directory, "*.html")):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                all_data.extend(extract_data(soup))
        except Exception as e:
            print(f"Ошибка при обработке файла '{filename}': {e}")

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

def process_data(json_filename, output_dir="output"):
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл '{json_filename}' не найден.")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка: не удалось декодировать JSON: {e}")
        return

    df = pd.DataFrame(data)

    df["price"] = pd.to_numeric(df["price"])

    df.fillna(0, inplace=True)

    sorted_df = df.sort_values("price", ascending=False)
    sorted_df.to_json(os.path.join(output_dir, "sorted_data.json"), orient="records", indent=4)

    filtered_df = df[df["sim"] == "2 SIM"]
    filtered_df.to_json(os.path.join(output_dir, "filtered_data.json"), orient="records", indent=4)

    price_stats = df["price"].agg(["sum", "min", "max", "mean", "std"])
    price_stats_dict = price_stats.to_dict()
    with open(os.path.join(output_dir, "price_stats.json"), "w") as f:
        json.dump(price_stats_dict, f, indent=4)

    matrix_counts = df["matrix"].value_counts().to_dict()
    with open(os.path.join(output_dir, "matrix_counts.json"), "w") as f:
        json.dump(matrix_counts, f, indent=4)

html_files_directory = "2"
output_json_file = "second.json"
output_directory = "2_output"
os.makedirs(output_directory, exist_ok=True)

parse_html_files(html_files_directory, output_json_file)
process_data(output_json_file, output_directory)
