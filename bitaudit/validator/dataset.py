import os
import random
from pathlib import Path
from huggingface_hub import snapshot_download
from bitaudit.utils.const import *
import pandas as pd


DOWNLOAD_FOLDER = Path('bitaudit/dataset')
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def download_dataset():
    # Specify your desired destination path
    repo_id = HUGGINGFACE_REPO_ID
    # Download the dataset to the specified path
    snapshot_download(repo_id=repo_id, local_dir=DOWNLOAD_FOLDER,
                      repo_type="dataset", token=HUGGINGFACE_TOKEN, force_download=False)


def generate_random_path():
    vulnerabilities_category = ["block number dependency",
                                "dangerous delegatecall",
                                "integer overflow",
                                "reentrancy vulnerability",
                                "timestamp dependency",
                                "unchecked external call"]

    random_category = random.choice(vulnerabilities_category)

    directory_path = f"bitaudit/dataset/smart_contract_dataset/{random_category}"

    # Get a list of all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # Check if the directory is not empty
    if files:
        # Choose a random file from the list
        random_file = random.choice(files)
        print("Randomly chosen file:", random_file)
    else:
        print("Directory is empty.")

    smart_contract_path = f"bitaudit/dataset/smart_contract_dataset/{random_category}/{random_file}"
    file_no = random_file.split('.')[0]
    return smart_contract_path, file_no


def preprocess_json(input_dict):
    processed_dict = {}
    for key, value in input_dict.items():
        # Stripping and lowercasing keys
        processed_key = key.strip().lower()

        # Stripping and lowercasing values
        if isinstance(value, str):
            processed_value = value.strip().lower()
        else:
            processed_value = value

        processed_dict[processed_key] = processed_value

    return processed_dict


def generate_labels(file_no):
    # Load the CSV file
    df = pd.read_csv("bitaudit/dataset/output.csv")

    # Filter the rows based on file number
    filtered_df = df[df['file'] == int(file_no)]

    # Check if 'ground truth' has a single unique value
    unique_ground_truth_values = filtered_df[filtered_df['ground truth'] == 1]
    label = {}
    if len(unique_ground_truth_values) > 0:
    # Add only the rows with a single unique value to the result list
        for index, row in unique_ground_truth_values.iterrows():
            label.update({row['contract']: row['error_type']})
    return label