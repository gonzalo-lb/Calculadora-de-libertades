import json

with open('test.json', encoding='utf-8') as testfile:
    test = json.load(testfile)

tprint = test['keyy']

print(tprint)