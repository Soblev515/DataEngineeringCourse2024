import xml.etree.ElementTree as ET
import json
import pandas as pd
import re
import os
import glob

def parse_xml_files(directory, output_filename="output.json"):
    all_data = []
    for filename in glob.glob(os.path.join(directory, "*.xml")):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            item_data = {
                "name": root.findtext("name"),
                "constellation": root.findtext("constellation"),
                "spectral-class": root.findtext("spectral-class"),
                "radius": float(clean_numeric_string(root.findtext("radius"))),
                "rotation": root.findtext("rotation"),
                "age": root.findtext("age"),
                "distance": float(clean_numeric_string(root.findtext("distance"))),
                "absolute-magnitude": float(clean_numeric_string(root.findtext("absolute-magnitude")))
            }
            all_data.append(item_data)
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")
        except ET.ParseError as e:
            print(f"Ошибка при парсинге файла '{filename}': {e}")
        except (ValueError, TypeError) as e:
            print(f"Ошибка при чтении числового значения в файле '{filename}': {e}")


    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

def clean_numeric_string(text):
    text = text.strip() 
    text = re.sub(r"[^0-9.]", "", text)
    return text.strip()


def process_data(json_filename, output_dir="output"):
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{json_filename}' не найден.")
        return

    df = pd.DataFrame(data)
   
    sorted_df = df.sort_values('name')
    sorted_df.to_json(os.path.join(output_dir, "sorted_data.json"), orient="records", indent=4)

    filtered_df = df[df['constellation'] == "Дева"]
    filtered_df.to_json(os.path.join(output_dir, "filtered_data.json"), orient="records", indent=4)

 
    stats = df['radius'].agg(['sum', 'min', 'max', 'mean', 'std'])
    stats_dict = stats.to_dict()
    with open(os.path.join(output_dir, "stats.json"), 'w') as f:
        json.dump(stats_dict, f, indent=4)
    freq = df['constellation'].value_counts().to_dict()
    with open(os.path.join(output_dir, "frequencies.json"), 'w') as f:
        json.dump(freq, f, indent=4)


xml_files_directory = "3"
output_json_file = "third.json"
output_directory = "3_output"
os.makedirs(output_directory, exist_ok=True)

parse_xml_files(xml_files_directory, output_json_file)
process_data(output_json_file, output_directory)
