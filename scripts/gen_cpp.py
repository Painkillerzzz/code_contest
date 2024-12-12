import json

with open('results/data.json', 'r') as f:
    data = json.load(f)
    
for i in data:
    with open(f'code/{i['question_id']}.cpp', 'w') as f:
        f.write(i['code_file'])