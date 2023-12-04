import sqlite3
import csv

# Database path
database_path = '../TechnicalDebtDataset.db'

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
    CASE 
        WHEN EXISTS (
            SELECT 1 
            FROM SZZ_FAULT_INDUCING_COMMITS SFIC 
            WHERE SFIC.projectID = GCC.projectID 
              AND SFIC.faultInducingCommitHash = GCC.commitHash
        ) THEN 1 
        ELSE 0 
    END AS fault_inducing_label
FROM 
    GIT_COMMITS_CHANGES GCC;
"""

# Execute the query
cursor.execute(query)
print("Executed the query")
# Fetching the results
# with open('diffs_with_fault_inducing_label.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     # Write the headers
#     csvwriter.writerow(['CommitHash', 'NewPath', 'Diff', 'FaultInducingLabel'])
#
#     # Stream rows to the CSV file
#     for row in cursor:
#         csvwriter.writerow(row)
#start
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

# Writing to CSV
with open('../diffs_with_fault_inducing_label.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the headers
    csvwriter.writerow(['CommitHash', 'NewPath', 'Diff', 'FaultInducingLabel'])

    # Stream rows to the CSV file
    for row in cursor:
        commit_hash, new_path, diff, fault_inducing_label = row
        if new_path.endswith('.java'):  # Check if file is a .java file
            truncated_diff = extract_added_lines(diff)
            if truncated_diff is not None:  # Write to CSV only if diff is under 2000 characters
                csvwriter.writerow([commit_hash, new_path, truncated_diff, fault_inducing_label])
#end

connection.close()

print("Written to CSV file")
