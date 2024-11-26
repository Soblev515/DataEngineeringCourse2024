import numpy as np
import json

matrix = np.load('first_task.npy')

total_sum = np.sum(matrix)
total_avr = np.mean(matrix)
main_diagonal = np.diagonal(matrix)
sum_md = np.sum(main_diagonal)
avr_md = np.mean(main_diagonal)
secondary_diagonal = np.diagonal(np.fliplr(matrix))
sum_sd = np.sum(secondary_diagonal)
avr_sd = np.mean(secondary_diagonal)
max_value = np.max(matrix)
min_value = np.min(matrix)

result = {
    "sum": int(total_sum),
    "avr": int(total_avr),
    "sumMD": int(sum_md),
    "avrMD": int(avr_md),
    "sumSD": int(sum_sd),
    "avrSD": int(avr_sd),
    "max": int(max_value),
    "min": int(min_value)
}

with open('first_task_out.json', 'w') as json_file:
    json.dump(result, json_file)
normalized_matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

np.save('first_task_out_matrix.npy', normalized_matrix)
