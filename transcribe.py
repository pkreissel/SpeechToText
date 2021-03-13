from wit import Wit
from pydub import AudioSegment
from pydub.silence import split_on_silence
from joblib import Parallel, delayed
from tqdm import tqdm
import os
from keys import WIT_KEY
import time


client = Wit(WIT_KEY)

sound = AudioSegment.from_mp3("file.mp3")
print("first split round, this might take a while")
chunks = split_on_silence(sound, min_silence_len=2000,silence_thresh=-30, seek_step=10)

def chunkexport(chunk, num, level):
    if(len(chunk) > 19000):
        subchunks = split_on_silence(chunk, min_silence_len= int(1000 / level) ,silence_thresh=-30)
        for i, subchunk in enumerate(subchunks):
            chunkexport(subchunk, num + "_" + str(i).zfill(4), level + 1)
    else:
        chunk.export("cache/chunk{0}.wav".format(num), format="wav")

print("second split round, this will run in parallel")
Parallel(n_jobs=12)(delayed(chunkexport)(chunk, str(i).zfill(5), 1) for i, chunk in enumerate(tqdm(chunks)))

text = []

def wit_file(file):
    time.sleep(2)
    if not file.endswith('.wav'):
        return None
    with open("cache/" + file, 'rb') as f:
        try:
            resp = client.speech(f, {'Content-Type': 'audio/wav'})
            os.remove("cache/" + file)
            return resp["text"] + "\n"
        except Exception as e:
            #print(resp)
            print(e)
            return None

text = Parallel(n_jobs=6)(delayed(wit_file)(file) for i, file in enumerate(tqdm(sorted(os.listdir("cache")))))

text

output = open("output.txt","a")
output.writelines([str for str in text if not str == None])
output.close()
