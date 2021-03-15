Still in early development, use with caution

# Infos
Wit.ai is free, but only allows only files with max-length 10s.
This script will iteratively try to cut audio of unlimited size into chunks of appropriate size, while (hopefully) respecting word boundaries.
Then the chunks are sent to wit and a textfile is exported.

# Install:

download this repo
cd into it
pip3 install -r requirements.txt

# Usage:

- Change WIT_KEY to your wit.ai key (free)
- Put files of most audio formats into "input" folder
- run python transcribe.py
- output file should be in "output" folder

For most Youtube Videos Youtube already created captions.
You can download those with yt_captions.py.
- Create a file input.txt with one Youtube Vid per Line
- Run python yt_captions.py
- SRT Files are being create

# TODO:
- ~~Empty Cache after run~~
- ~~Different File Types~~
- ~~Performance Improvements on first split~~
- Reuse Info from first split?
- Files via Command Line Arguments
