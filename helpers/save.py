import os
import json

class Store(object):
    _instances = {}
    data = {}
    def __new__(cls, path, *args, **kwargs):
        if path not in Store._instances:
            print("creating instance at", path)
            Store._instances[path] = super(Store, cls).__new__(cls, *args, **kwargs)
        return Store._instances[path]

    def __init__(self, path):
        if not self.data:
            self.dir = os.path.dirname(path)
            self.config_file = f"{path}.json"
            self.data = self.load()
            self.autosave = False

    def load(self):
        data = {}
        if os.path.isfile(self.config_file):
            print("Loading ", self.config_file)
            with open(self.config_file, "r") as f:
                data.update(json.load(f))
        else:
            print("no file", self.config_file)
        return data

    def save(self):
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f)

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def __setitem__(self, key, value):
        self.data[key] = value
        if self.autosave:
            self.save()
    
    def __contains__(self, key):
        return self.data.__contains__(key)
        
    def __delitem__(self, key):
        del self.data[key]
        if sef.autosave:
            self.save()

def get_save(guild_id, name, sub_folder=None):
    if sub_folder:
        return Store(os.path.join("guilds", str(guild_id), sub_folder, name))
    return Store(os.path.join("guilds", str(guild_id), name))
