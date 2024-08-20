import configparser

def read_ini_file(path_to_ini):
    config = configparser.ConfigParser()
    if not config.read(path_to_ini):
        raise FileNotFoundError(f"Error loading commands from {path_to_ini}. File not found.")
    return config

def get_json_file_path(config):
    try:
        return config.get('paths', 'json_file')
    except Exception as e:
        print(f"Failed to read configuration: {e}")
        return None
