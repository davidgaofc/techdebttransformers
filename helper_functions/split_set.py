import pandas as pd
from sklearn.model_selection import train_test_split

def split_csv(file_path, train_size=0.8, validation_size=0.2, test_size=0.2):
    """
    Split a CSV file into training, validation, and test datasets while maintaining
    similar distributions of labels.

    Args:
    file_path (str): Path to the CSV file.
    train_size (float): Proportion of the dataset to include in the train split.
    validation_size (float): Proportion of the dataset to include in the validation split.
    test_size (float): Proportion of the dataset to include in the test split.

    Returns:
    Three DataFrames corresponding to the train, validation, and test datasets.
    """

    # Load the data from the CSV file
    data = pd.read_csv(file_path)

    #remove empty diffs
    data = data[data['Diff'].notna()]
    #remove diffs that are ""
    data = data[data['Diff'] != ""]
    data = data[~data['Diff'].str.startswith("//")]

    # Remove rows with only whitespace
    data = data[data['Diff'].str.strip() != ""]

    # Remove rows where the length of the diff is null
    data = data[data['Diff'].str.len().notna()]
    data = data[data['Diff'].str.replace(r'\s+', '', regex=True).str.len() >= 5]

    # Split the data into training and temp (validation + test) sets
    train_data, test_data = train_test_split(data, train_size=train_size)

    # Split the temp data into validation and test sets
    # validation_data, test_data = train_test_split(temp_data, test_size=test_size/(test_size + validation_size))

    train_data.to_csv('../gen_data/train_data.csv', index=False)
    # validation_data.to_csv('../gen_data/validation_data.csv', index=False)
    test_data.to_csv('../gen_data/test_data.csv', index=False)

    print("Data successfully split and saved into train_data.csv, validation_data.csv, and test_data.csv")
    # return train_data, validation_data, test_data
    return 0,0,0

train_data, validation_data, test_data = split_csv('../diffs_with_sonar_message.csv')

