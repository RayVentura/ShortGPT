import yaml
import os
from dotenv import load_dotenv

load_dotenv()

ELEVEN_LABS_KEY = os.getenv('ELEVEN_LABS_API_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
PLAY_HT_USERID = os.getenv('PLAY_HT_USERID')
PLAY_HT_API_KEY = os.getenv('PLAY_HT_API_KEY')


def read_yaml_config(file_path: str) -> dict:
    """Reads and returns the contents of a YAML file as dictionary"""
    with open(file_path, 'r') as file:
        contents = yaml.safe_load(file)
    return contents

def write_yaml_config(file_path: str, data: dict):
    """Writes a dictionary to a YAML file"""
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def load_editing_assets() -> dict:
    """Loads all local assets from the static-assets folder specified in the yaml_config"""
    yaml_config = read_yaml_config("public.yaml")
    if yaml_config['local-assets'] == None:
        yaml_config['local-assets'] = {}
    # Create a copy of the dictionary before iterating over it
    local_paths = []
    if yaml_config['local-assets'] != {}:
        local_assets = yaml_config['local-assets'].copy()
        # Removing local paths that don't exist
        for key in local_assets:
            asset = local_assets[key]
            if(type(asset) == str):
                filePath = local_assets[key]
            else:
                filePath = local_assets[key]['path']
            if not os.path.exists(filePath):
                del yaml_config['local-assets'][key]
            else:
                local_paths.append(filePath)

    folder_path = 'public'
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename).replace("\\", "/")
            if not file_path in local_paths:
                yaml_config['local-assets'][filename] = file_path

    write_yaml_config("public.yaml", yaml_config)

    return yaml_config


# print(load_editing_assets())
# print(read_yaml_config("editing_assets.yaml")['local-assets'])
