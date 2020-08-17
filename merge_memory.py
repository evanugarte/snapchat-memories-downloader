import os
import subprocess
from datetime import datetime


class MemoriesMerger:
    path_to_memories = None
    memories = []

    def __init__(self, path_to_memories):
        self.path_to_memories = path_to_memories

    def load_memories(self):
        # load only .mp4 files
        self.memories = [memory for memory
                         in os.listdir(self.path_to_memories)
                         if '.mp4' in memory]

    def handle_merge(self):
        files_to_merge = []

        for i in range(len(self.self.memories) - 1):
            memory_a = self.memories[i]
            memory_b = self.memories[i+1]

            date_a = datetime.strptime(
                memory_a.split('.')[0], '%Y-%m-%d,%H:%M:%S')
            date_b = datetime.strptime(
                memory_b.split('.')[0], '%Y-%m-%d,%H:%M:%S')
            # if memory_a and memory_b are within
            # ten seconds of eachother weshould merge
            if abs(date_a - date_b).seconds <= 10:
                print(f'i need to merge {memory_a} and {memory_b}')
                # there may be a case where more than two memories
                # need to be merged. in this case we make sure we
                # havent already marked a memory to merged.
                if memory_a not in files_to_merge:
                    os.system(
                        f"echo file \\'{self.path_to_memories+memory_a}\\' >> merge_list.txt")
                    files_to_merge.append(memory_a)
                os.system(
                    f"echo file \\'{self.path_to_memories+memory_b}\\' >> merge_list.txt")
                files_to_merge.append(memory_b)
            else:
                # if the two memories do not need to be merged, we check if we
                # have an existing list to merge and handle if so
                if len(files_to_merge):
                    print('i am merging', files_to_merge)
                    # use ffmpeg and concat to handle the merge and output it
                    # to a merged directory
                    os.system(
                        f'ffmpeg -f concat -safe 0 -i merge_list.txt -c copy \
                        {self.path_to_memories}/merged/{files_to_merge[0]} >/dev/null 2>&1')
                    os.system(f"echo > merge_list.txt")
                    # delete the videos we have now merged into one
                    for part_of_video in files_to_merge:
                        print('deleting', self.path_to_memories + part_of_video)
                        os.system(
                            f'rm -rf {self.path_to_memories + part_of_video}')
                    files_to_merge.clear()


if __name__ == "__main__":
    PATH_TO_HDD = '/media/evan/72E93F4E4DD7285D/snapchat_temp/'
    memories_merger = MemoriesMerger(PATH_TO_HDD)
    memories_merger.load_memories()
    memories_merger.handle_merge()
