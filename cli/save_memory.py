import json
import os
from os import path
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait


class MemoriesDownloader:
    def __init__(self, path_to_json, download_location, thread_count=10):
        self.path_to_json = path_to_json
        self.download_location = download_location
        self.thread_count = thread_count
        self.data = None

    def split_into_n_parts(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def load_json(self):
        # for the number of threads we have, split the memories json
        # into equal parts
        with open(self.path_to_json) as f:
            self.data = json.load(f)
        self.split_memories = list(self.split_into_n_parts(self.data,
                                                           self.thread_count))

    def handle_download(self, memories_list):
        for memory in memories_list:
            print('downloading', memory['date'])
            # get the full path to the memory we are about to save
            # e.g. /path/to/memory/2020-08-16,19:12:45.mp4
            file_path = path.join(self.download_location,
                                  f'{memory["date"]}.{memory["fileType"]}')
            url = memory['awsLink']
            r = requests.get(url)
            with open(file_path, 'wb') as f:
                # download the memory to the location specified
                f.write(r.content)
            print('finished', file_path)

    def download_memories(self):
        # create ten threads for
        executor = ThreadPoolExecutor(self.thread_count)
        # have each thread go about downloading its share of memories
        futures = [executor.submit(self.handle_download, memories)
                   for memories in self.split_memories]
        wait(futures)


if __name__ == "__main__":
    PATH_TO_JSON = os.getcwd() + '/aws_links.json'
    PATH_TO_HDD = os.getcwd() + '/snapchat_temp/'
    m = MemoriesDownloader(PATH_TO_JSON, PATH_TO_HDD)
    m.load_json()
    m.download_memories()
