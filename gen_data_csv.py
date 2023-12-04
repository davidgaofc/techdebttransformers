import sqlite3
import csv

# Database path
database_path = 'TechnicalDebtDataset.db'

# Connecting to the SQLite database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()
print("Connected to SQLite")
# SQL Query to join GIT_COMMITS_CHANGES and SZZ_FAULT_INDUCING_COMMITS
query = """
SELECT 
    GCC.commitHash, 
    GCC.newPath,
    GCC.diff,
    (SELECT SI.message
     FROM SONAR_ISSUES SI 
     WHERE SI.projectID = GCC.projectID 
       AND SI.creationCommitHash = GCC.commitHash
     LIMIT 1) AS message
FROM 
    GIT_COMMITS_CHANGES GCC
WHERE EXISTS (
    SELECT 1
    FROM SONAR_ISSUES SI 
    WHERE SI.projectID = GCC.projectID 
      AND SI.creationCommitHash = GCC.commitHash
    LIMIT 1
);
"""

# Execute the query
cursor.execute(query)
print("Executed the query")

# total_rows = 0
# total_java = 0
# for row in cursor:
#     if('.java' in row[1] and row[3] is not None):
#         total_java += 1
#     total_rows += 1
#     print(total_java, total_rows)
#
# print("Total rows: ", total_rows)
# print("Total java files: ", total_java)

def extract_added_lines(diff, max_length=2000):
    added_lines = []
    for line in diff.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            added_line = line[1:]  # Remove the '+' sign
            if sum(len(l) + 1 for l in added_lines) + len(added_line) <= max_length:
                added_lines.append(added_line)
            else:
                return None
                break
    return '\n'.join(added_lines)


with open('diffs_with_sonar_message.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the headers
    csvwriter.writerow(['CommitHash', 'NewPath', 'Diff', 'Message'])

    # Stream rows to the CSV file
    for row in cursor:
        commit_hash, new_path, diff, fault_inducing_label = row
        if new_path.endswith('.java'):  # Check if file is a .java file
            truncated_diff = extract_added_lines(diff)
            if truncated_diff is not None:  # Write to CSV only if diff is under 2000 characters
                csvwriter.writerow([commit_hash, new_path, truncated_diff, fault_inducing_label])

connection.close()

print("Written to CSV file")
