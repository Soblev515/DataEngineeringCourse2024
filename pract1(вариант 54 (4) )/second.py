input_file = "second_task.txt"
output_file = "second_task_out.txt"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
results = []
for line in lines:
    numbers = [int(x) for x in line.split() if int(x) > 0]
    sum_pos = sum(numbers)
    average_pos = sum_pos/len(numbers)
    results.append(average_pos)

max_val = max(results)
min_val = min(results)

with open(output_file, 'w') as outfile:
    for result in results:
        outfile.write(str(result) + "\n")
    outfile.write("\n")
    outfile.write(f"{max_val}\n")
    outfile.write(f"{min_val}\n")
