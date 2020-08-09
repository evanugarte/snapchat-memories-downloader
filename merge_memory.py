import os
import subprocess
from datetime import datetime

PATH_TO_HDD = '/media/evan/72E93F4E4DD7285D/snapchat_temp/'


def main():
    memories = [memory for memory
                in os.listdir(PATH_TO_HDD)
                if '.mp4' in memory]

    file_just_added = []

    for i in range(len(memories) - 1):
        memory_a = memories[i]
        memory_b = memories[i+1]

        date_a = datetime.strptime(memory_a.split('.')[0], '%Y-%m-%d,%H:%M:%S')
        date_b = datetime.strptime(memory_b.split('.')[0], '%Y-%m-%d,%H:%M:%S')

        if abs(date_a - date_b).seconds <= 10:
            print(f'i need to merge {memory_a} and {memory_b}')
            if memory_a not in file_just_added:
                os.system(f"echo file \\'{PATH_TO_HDD+memory_a}\\' >> lol.txt")
                file_just_added.append(memory_a)
            os.system(f"echo file \\'{PATH_TO_HDD+memory_b}\\' >> lol.txt")
            file_just_added.append(memory_b)
        else:
            if len(file_just_added):
                print('i am merging', file_just_added)
                os.system(
                    f'ffmpeg -f concat -safe 0 -i lol.txt -c copy /media/evan/72E93F4E4DD7285D/merged/{file_just_added[0]} >/dev/null 2>&1')
                os.system(f"echo > lol.txt")
                file_just_added.clear()


def rename_to_comma():
    for memory in os.listdir(PATH_TO_HDD):
        name_with_comma = ','.join([x for x in memory.split(' ')])
        print(name_with_comma)
        os.rename(PATH_TO_HDD + memory, PATH_TO_HDD + name_with_comma)


main()
