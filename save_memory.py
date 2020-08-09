import json
import os
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait


class MemoriesDownloader:
    MONTH_MAP = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def split_into_n_parts(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def load_json(self):
        with open(self.file_path) as f:
            self.data = json.load(f)
        self.split_memories = list(self.split_into_n_parts(self.data, 10))

    def ensure_directory_exists(self, memory):
        if not os.path.isdir(f'/media/evan/72E93F4E4DD7285D/snapchat/{memory["year"]}/'):
            os.mkdir(f'/media/evan/72E93F4E4DD7285D/snapchat/{memory["year"]}')
        if not os.path.isdir(f'/media/evan/72E93F4E4DD7285D/snapchat/{memory["year"]}/{self.MONTH_MAP[memory["month"]]}/'):
            os.mkdir(
                f'/media/evan/72E93F4E4DD7285D/snapchat/{memory["year"]}/{self.MONTH_MAP[memory["month"]]}/')
        if not os.path.isdir(f'/media/evan/72E93F4E4DD7285D/snapchat/{memory["year"]}/{self.MONTH_MAP[memory["month"]]}/{memory["day"]}/'):
            os.mkdir(
                f'/media/evan/72E93F4E4DD7285D/snapchat/{memory["year"]}/{self.MONTH_MAP[memory["month"]]}/{memory["day"]}/')

    def handle_download(self, memories_list):
        for memory in memories_list:
            print('downloading', memory['date'])
            # self.ensure_directory_exists(memory)
            # file_path = f'/media/evan/72E93F4E4DD7285D/snapchat/{memory["year"]}/{self.MONTH_MAP[memory["month"]]}/{memory["day"]}/{memory["time"]}.{memory["fileType"]}'
            file_path = f'/media/evan/72E93F4E4DD7285D/snapchat_temp/{memory["date"]}.{memory["fileType"]}'
            url = memory['awsLink']
            r = requests.get(url)
            with open(file_path, 'wb') as f:
                f.write(r.content)
            print('finished', file_path)

    def download_memories(self):
        executor = ThreadPoolExecutor(10)
        futures = [executor.submit(self.handle_download, memories)
                   for memories in self.split_memories]
        wait(futures)


m = MemoriesDownloader('/home/evan/Documents/snapchat/aws_links_4160.json')
m.load_json()
m.download_memories()

# get length of json

# for n threads split indexes into n parts
