import numpy as np
import math
input_file = "third_task.txt"
output_file = "third_task_out.txt"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(output_file, 'w') as outfile:
    for line in lines:
        row_data = line.strip().split()
        numeric_row = []
        for item in row_data:
            if item == "NA" or item == "N/A":
                numeric_row.append(np.nan)
            else:
                numeric_row.append(float(item))

        numeric_array = np.array(numeric_row)

        nan_indices = np.isnan(numeric_array)
        numeric_array[nan_indices] = np.nanmean(numeric_array)
        filtered_array = numeric_array[(numeric_array > 0) & (np.sqrt(numeric_array) > 50)]

        row_sum = np.sum(filtered_array)
        outfile.write(str(row_sum) + "\n")
