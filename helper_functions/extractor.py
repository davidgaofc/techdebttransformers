import sqlite3

database_path = '../TechnicalDebtDataset.db'

connection = sqlite3.connect(database_path)

cursor = connection.cursor()


query = "SELECT oldpath, newpath , diff FROM GIT_COMMITS_CHANGES;"

cursor.execute(query)

#remove comments
#only look at added lines
#https://huggingface.co/docs/transformers/tasks/sequence_classification#evaluate
#https://www.tensorflow.org/text/tutorials/classify_text_with_bert


result = cursor.fetchall()
# temp = result[5][0]
long_counter = 0
total_counter = 0
java_counter = 0
# print(result[4])
# my_max = 0
for i in result:
    if(".java" in i[1]):
        print(len(i[2]))
        if(len(i[2]) < 2000):
            long_counter += 1

        java_counter += 1
    total_counter += 1
print(long_counter)
print(java_counter)
print(total_counter)


# for i in result:
#     print(i)

cursor.close()
connection.close()