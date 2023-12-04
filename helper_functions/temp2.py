import csv

# Specify the path to your CSV file
file_path = '../data/train_data.csv'

# Reading the first three lines of the CSV file
debt_counter = 0
total_counter = 0
with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if(row[3] == "1"):
            debt_counter += 1
        total_counter += 1

print(debt_counter)
print(total_counter)
print(debt_counter/total_counter)