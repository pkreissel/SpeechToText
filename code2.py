from wit import Wit
import logging
from pydub import AudioSegment
from pydub.silence import split_on_silence
from joblib import Parallel, delayed
from tqdm import tqdm
import os

WIT_KEY = ""
client = Wit(WIT_KEY)

sound = AudioSegment.from_mp3("file.mp3", format = "mp3")
chunks = split_on_silence(sound, min_silence_len=2000,silence_thresh=-30)

def chunkexport(chunk, num, level):
    if(len(chunk) > 19000):
        subchunks = split_on_silence(chunk, min_silence_len= int(1000 / level) ,silence_thresh=-30)
        for i, subchunk in enumerate(subchunks):
            chunkexport(subchunk, num + "_" + str(i).zfill(4), level + 1)
    else:
        chunk.export("cache/chunk{0}.wav".format(num), format="wav")

Parallel(n_jobs=12)(delayed(chunkexport)(chunk, str(i).zfill(5), 1) for i, chunk in enumerate(tqdm(chunks)))

text = []

for i, file in enumerate(tqdm(sorted(os.listdir("cache")))):
    if not file.endswith('.wav'):
        continue
    print(file)
    with open("cache/" + file, 'rb') as f:
        try:
            resp = client.speech(f, {'Content-Type': 'audio/wav'})
            text.append(resp["text"])
        except Exception as e:
            print(e)

output = open("output.txt","a")
output.writelines(text)
output.close()
