import sqlite3


# Database path
database_path = '../TechnicalDebtDataset.db'

# Connecting to the SQLite database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()
print("Connected to SQLite")
# SQL Query to join GIT_COMMITS_CHANGES and SZZ_FAULT_INDUCING_COMMITS
query1 = """
SELECT diff FROM GIT_COMMITS_CHANGES WHERE commithash = 'ed205c04fc8f9c95bc498d51e6fec3a6a052ca11';
"""

query = """
SELECT 
    (SELECT COUNT(DISTINCT commitHash) FROM GIT_COMMITS_CHANGES) AS TotalCommits,
    (SELECT COUNT(DISTINCT creationCommitHash) FROM SONAR_ISSUES) AS FaultInducingCommits,
    (SELECT COUNT(DISTINCT creationCommitHash) FROM SONAR_ISSUES) * 100.0 / (SELECT COUNT(DISTINCT commitHash) FROM GIT_COMMITS_CHANGES) AS FaultInducingPercentage
"""

cursor.execute(query1)

result = cursor.fetchall()

print(result)