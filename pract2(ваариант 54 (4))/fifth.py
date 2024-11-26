import pandas as pd
import numpy as np
import os
import json
import msgpack
import cloudpickle

data = pd.read_csv('kaggle_london_house_price_data.csv')

selected_columns = ['fullAddress', 'outcode', 'currentEnergyRating', 'rentEstimate_lowerPrice', 'rentEstimate_currentPrice', 'rentEstimate_upperPrice', 'floorAreaSqM']
data = data[selected_columns]

numeric_stats = {}
for column in data.select_dtypes(include=[np.number]).columns:
    numeric_stats[column] = {
        'max': data[column].max(),
        'min': data[column].min(),
        'mean': data[column].mean(),
        'sum': data[column].sum(),
        'std': data[column].std()
    }

categorical_stats = {}
for column in data.select_dtypes(include=[object]).columns:
    categorical_stats[column] = data[column].value_counts().to_dict()
    
stats = {
    'numeric_stats': numeric_stats,
    'categorical_stats': categorical_stats
}
with open('fifth.json', 'w') as json_file:
    json.dump(stats, json_file, indent=4)

data.to_csv('fifth.csv', index=False)
data.to_json('fifth.json', orient='records', lines=True)
with open("fifth.msgpack", "wb") as f:
    msgpack.pack(data.to_dict(orient="records"), f)
with open("fifth.pkl", "wb") as f:
    cloudpickle.dump(data, f)
