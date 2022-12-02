import json

with open('test.json', encoding='utf-8') as file:
    data = json.load(file)

print(data['Llave']['Denominacion'])