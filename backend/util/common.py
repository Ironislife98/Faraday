import os
import json


# Skips having to rewrite the same code in nearly every file
def load_config() -> dict:
    with open(os.path.join(os.getcwd(), "config.faraday.json")) as f:
        data: dict = json.load(f)
    return data
