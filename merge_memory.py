import os
import subprocess
from datetime import datetime

PATH_TO_HDD = '/media/evan/72E93F4E4DD7285D/snapchat_temp/'


def main():
    memories = [memory for memory
                in os.listdir(PATH_TO_HDD)
                if '.mp4' in memory]

    files_to_merge = []

    for i in range(len(memories) - 1):
        memory_a = memories[i]
        memory_b = memories[i+1]

        date_a = datetime.strptime(memory_a.split('.')[0], '%Y-%m-%d,%H:%M:%S')
        date_b = datetime.strptime(memory_b.split('.')[0], '%Y-%m-%d,%H:%M:%S')

        if abs(date_a - date_b).seconds <= 10:
            print(f'i need to merge {memory_a} and {memory_b}')
            if memory_a not in files_to_merge:
                os.system(f"echo file \\'{PATH_TO_HDD+memory_a}\\' >> lol.txt")
                files_to_merge.append(memory_a)
            os.system(f"echo file \\'{PATH_TO_HDD+memory_b}\\' >> lol.txt")
            files_to_merge.append(memory_b)
        else:
            if len(files_to_merge):
                print('i am merging', files_to_merge)
                os.system(
                    f'ffmpeg -f concat -safe 0 -i lol.txt -c copy /media/evan/72E93F4E4DD7285D/merged/{files_to_merge[0]} >/dev/null 2>&1')
                os.system(f"echo > lol.txt")
                for part_of_video in files_to_merge:
                    print('deleting', PATH_TO_HDD + part_of_video)
                    os.system(f'rm -rf {PATH_TO_HDD + part_of_video}')
                files_to_merge.clear()


def rename_to_comma():
    for memory in os.listdir(PATH_TO_HDD):
        name_with_comma = ','.join([x for x in memory.split(' ')])
        print(name_with_comma)
        os.rename(PATH_TO_HDD + memory, PATH_TO_HDD + name_with_comma)


main()
