# snapchat-memories-downloader
This tool saves all your memories to your computer after you download your data from Snapchat.

## How to Download Memories
### From the Website
Visit [snapchat-memory-saver.com](https://www.snapchat-memory-saver.com/)

### Using the [`cli`](https://github.com/evanugarte/snapchat-memories-downloader/tree/master/cli) directory
(make sure node and python3 are installed before!)
1. Request your data from snapchat ([tutorial](https://youtu.be/ipjvQt-ZCkA?t=52))
1. Extract the `memories_history.json` file from your data.
1. Place the `memories_history.json` file in the [`cli`](https://github.com/evanugarte/snapchat-memories-downloader/tree/master/cli) directory
1. Run the file to get the S3 links with `node generate_aws.js` from within the above directory.
1. Run the file to download your snapchat data with `python save_memory.py` from within the above directory.

## Tutorial Videos
Check out [Part 1](https://www.youtube.com/watch?v=NMZ-ClP3-ew) and [Part 2](https://www.youtube.com/watch?v=ZOiCIyJck_c) on YouTube!
