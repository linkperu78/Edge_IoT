import json

def get_json_from_file(json_file):
    extension = ".json"
    path = json_file
    if not (extension in json_file):
        path = json_file.split(".")[0]
        path = path + extension
    with open("json_values/" + path, 'r') as file:
        return json.load(file)
    
def save_in_json_file(json_file, data):
    extension = ".json"
    path = json_file
    if not (extension in json_file):
        path = json_file.split(".")[0]
        path = path + extension
    path = "json_values/" + path
    with open(path, 'w') as file:
        json.dump(data, file)