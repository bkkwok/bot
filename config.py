import json


def configFile():
    with open('config.json') as file:
        config = json.loads(file.read())

        return config

