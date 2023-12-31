import json


def load_config_from_json(file_path: str):
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config

def save_config_to_json(file_path: str, config: dict):
    with open(file_path, 'w') as f:
        json.dump(config, f, indent=2)
