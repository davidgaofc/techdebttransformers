import sqlite3


# Database path
database_path = '../TechnicalDebtDataset.db'

# Connecting to the SQLite database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()
print("Connected to SQLite")
# SQL Query to join GIT_COMMITS_CHANGES and SZZ_FAULT_INDUCING_COMMITS
query = """
SELECT 
    GCC.diff
FROM 
    GIT_COMMITS_CHANGES GCC
WHERE
    GCC.commitHash = 'e0880e263e4bf8662ba3848405200473a25dfc9f'
;
"""

# Execute the query
cursor.execute(query)
print("Executed the query")

result = cursor.fetchall()

for i in result:
    print(i[0])
    print("--------------------------------------------------")
