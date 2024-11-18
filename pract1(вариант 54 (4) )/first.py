import re
from collections import Counter
input_file = "first_task.txt"
output_file = "first_task_out.txt"
var_output_file = "first_task_out_var.txt"
with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()
text = re.sub(r'[^\w\s]', '', text).lower()
words = text.split()
word_counts = Counter(words)
sorted_word_counts = word_counts.most_common()
consonant_count = 0
for word in words:
    if len(word)>4:
        consonant_count += 1
total_words = len(words)
consonant_proportion = consonant_count / total_words if total_words > 0 else 0
with open(output_file, "w", encoding='utf-8') as outfile:
    for word, count in sorted_word_counts:
        outfile.write(f"{word}:{count}\n")
with open(var_output_file, "w", encoding='utf-8') as outfile:    
    outfile.write(f"Слов, начинающихся на согласную: {consonant_count}\n")
    outfile.write(f"Доля слов, начинающихся на согласную: {consonant_proportion:.4f}\n")
