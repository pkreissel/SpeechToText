Still in early development, use with caution

# Infos
Wit.ai is free, but only allows only files with max-length 10s.
This script will iteratively try to cut audio of unlimited size into chunks of appropriate size, while (hopefully) respecting word boundaries.
Then the chunks are sent to wit and a textfile is exported.

# Install:

pip3 install -r requirements.txt

# Usage:

- Change WIT_KEY to your wit.ai key (free)
- Put file.mp3 into folder
- run python transcribe.py

# TODO:
- Empty Cache after run
- Different File Types
- Performance Improvements on first split
- Reuse Info from first split?
- Files via Command Line Arguments
