import json


def load_json_file(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def load_accounts(path):
    raw_data = load_json_file(path)
    return raw_data['credentials']
