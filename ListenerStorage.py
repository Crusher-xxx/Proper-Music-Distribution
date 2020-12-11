import Listener
import json


class ListenerStorage:
    def __init__(self):
        self.listeners: list[Listener.Listener] = []
        self.path = r'D:\REPOS\ProperMusicDistribution\data.json'

    def __getitem__(self, item):
        return self.listeners[item]

    def append(self, listener):
        self.listeners.append(listener)

    def save(self):
        list_of_dictionaries = [dict(x) for x in self.listeners]
        with open(self.path, 'w', encoding='utf8') as outfile:
            json.dump(list_of_dictionaries, outfile, ensure_ascii=False, indent=4)

    def load(self):
        with open(self.path, 'r', encoding='utf8') as json_file:
            list_of_dictionaries = json.load(json_file)
            self.listeners = [Listener.Listener.from_dictionary(x) for x in list_of_dictionaries]
