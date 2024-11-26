import json
import msgpack
import os

with open('third_task.json', 'r') as json_file:
    products = json.load(json_file)


aggregated_data = []
for product in products:
    prices = product.get('prices', [])
    if prices:
        avg_price = sum(prices) / len(prices)
        max_price = max(prices)
        min_price = min(prices)
        aggregated_data.append({
            'product_id': product['id'],
            'average_price': avg_price,
            'max_price': max_price,
            'min_price': min_price
        })

with open('third_task_out.json', 'w') as json_file:
    json.dump(aggregated_data, json_file, indent=4)

with open('third_task_out.msgpack', 'wb') as msgpack_file:
    msgpack.pack(aggregated_data, msgpack_file)
