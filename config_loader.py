# config_loader.py

import yaml

def load_config(stage_name: str):
    with open("config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config.get(stage_name, {})
