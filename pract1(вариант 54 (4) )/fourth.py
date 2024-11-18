import pandas as pd
import numpy as np
input_file = "fourth_task.txt"
output_summary_file = "fourth_task_out_summary.txt"
output_file = "fourth_task_out.txt"

df = pd.read_csv(input_file)
df = df.drop(columns=['rating'])
average_price = df['price'].mean()
max_quantity = df['quantity'].max()
min_price = df['price'].min()    
filtered_df = df[df['price'] > 7911]
with open(output_summary_file, 'w') as f:
    f.write(str(average_price) + '\n')
    f.write(str(max_quantity) + '\n')
    f.write(str(min_price) + '\n')

filtered_df.to_csv(output_file, index=False)
