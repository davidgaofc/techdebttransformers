import sqlite3

database_path = 'TechnicalDebtDataset.db'

connection = sqlite3.connect(database_path)

cursor = connection.cursor()


query = "PRAGMA table_info(SONAR_ISSUES);"

cursor.execute(query)


result = cursor.fetchall()
for i in result:
    print(i)

cursor.close()
connection.close()