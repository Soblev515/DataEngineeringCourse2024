import numpy as np

matrix = np.load('second_task.npy')
threshold_value = 5  
indices = np.argwhere(matrix > threshold_value)
values = matrix[matrix > threshold_value]

row_indices = indices[:, 0] 
col_indices = indices[:, 1]  


np.savez('second_task_out.npz', row_indices=row_indices, col_indices=col_indices, values=values)

np.savez_compressed('second_task_out_compressed.npz', row_indices=row_indices, col_indices=col_indices, values=values)
