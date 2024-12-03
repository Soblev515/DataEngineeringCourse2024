import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
import glob

def parse_xml_files(directory, output_filename="output.json"):
    all_data = []
    for filename in glob.glob(os.path.join(directory, "*.xml")):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            for clothing in root.findall('clothing'):
                item_data = {}
                for element in clothing:
                    item_data[element.tag] = element.text.strip()
                all_data.append(item_data)
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")
        except ET.ParseError as e:
            print(f"Ошибка при парсинге XML: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка при обработке файла '{filename}': {e}")

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

    df = df.fillna(0) 

    numeric_cols = ['id', 'price', 'rating', 'reviews']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    sorted_df = df.sort_values('price', ascending=False)
    sorted_df.to_json(os.path.join(output_dir, "sorted_data.json"), orient="records", indent=4)

    filtered_df = df[df['category'] == 'Sweater']
    filtered_df.to_json(os.path.join(output_dir, "filtered_data.json"), orient="records", indent=4)

    price_stats = df['price'].agg(['sum', 'min', 'max', 'mean', 'std'])
    price_stats_dict = price_stats.to_dict()
    with open(os.path.join(output_dir, "price_stats.json"), 'w') as f:
        json.dump(price_stats_dict, f, indent=4)

    category_counts = df['category'].value_counts().to_dict()
    with open(os.path.join(output_dir, "category_counts.json"), 'w') as f:
        json.dump(category_counts, f, indent=4)

    print(f"Обработка завершена. Результаты сохранены в '{output_dir}'.")

xml_files_directory = "4"
output_json_file = "four.json"
output_directory = "4_output"
os.makedirs(output_directory, exist_ok=True)


parse_xml_files(xml_files_directory, output_json_file)
process_data(output_json_file, output_directory)
