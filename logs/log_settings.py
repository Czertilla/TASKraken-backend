import logging.config
from json import load

with open("logs/presets/main.json", 'rb') as f:
    LOGGING = load(f)

def config():
    logging.config.dictConfig(LOGGING)

if __name__ =="__main__":
    config()