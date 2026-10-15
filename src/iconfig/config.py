import json


class Config:

    api_url=""
    api_key=""
    model= ""

    def __init__(self, config_file="config\\config.json"):
        with open(config_file, "r") as f:
            self.config = json.load(f)
            self.api_url=self.config["api_url"]
            self.api_key=self.config["api_key"]
            self.model=self.config["model"]



