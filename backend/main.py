import os
import json

FORMAT: str = 'utf-8'


with open(os.path.join(os.getcwd(), "config.faraday.json")) as f:
    config: dict = json.load(f)
