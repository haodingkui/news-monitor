import csv
from app import get_named_entities

csv_file = open("15test_data.csv", "r")
reader = csv.reader(csv_file)

new_csv_file = open('processed_data.csv', 'w')


for line in reader:
    title = line[1]
    url = line[2]
    time = line[3]
    content = line[4].replace(" ", "")
    if len(content) > 130:
        content = content[0:130]
    named_entities = get_named_entities(content)
    new_csv_file.write(",".join([title,url,time,'"' + str(named_entities) + '"']) + "\n")

new_csv_file.close()
csv_file.close()
