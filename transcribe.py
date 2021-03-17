from wit import Wit
from pydub import AudioSegment
from pydub.silence import split_on_silence
from joblib import Parallel, delayed
from tqdm import tqdm
import os
from keys import WIT_KEY
import time
import sys
import numpy as np

client = Wit(WIT_KEY)


for i, input in enumerate(tqdm(sorted(os.listdir("input")))):
    if input.startswith('.'):
        continue
    FILE_NAME = "input/" + input

    sound = AudioSegment.from_file(FILE_NAME, FILE_NAME.split(".")[1])

    if len(sound) > 10*60*1000:
        chunks = [sound[i*(int(len(sound)/12)):(i+1)*(int(len(sound)/12))] for i in range(0, 12)]
    else:
        chunks = split_on_silence(sound, min_silence_len=2000,silence_thresh=-30, seek_step=5)


    def chunkexport(chunk, num, level):
        if(len(chunk) > 19000):
            subchunks = split_on_silence(chunk, min_silence_len= int(1000 / level) ,silence_thresh=-30, keep_silence = True, seek_step=5)
            if len(subchunks) < 2:
                subchunks = [chunk[i*(int(len(chunk)/3)):(i+1)*(int(len(chunk)/3))] for i in range(0,3)]
            timestamps = []
            for i, subchunk in enumerate(subchunks):
                timestamps.append(chunkexport(subchunk, num + "_" + str(i).zfill(3), level + 1))
            return timestamps
        else:
            try:
                chunk.export("cache/chunk{0}.mp3".format(num), format="mp3")
                return(len(chunk))
            except Exception as e:
                return(len(chunk))
                print(e)

    print("second split round, this will run in parallel")
    timestamps_initial = Parallel(n_jobs=12)(delayed(chunkexport)(chunk, str(i).zfill(3), 1) for i, chunk in enumerate(tqdm(chunks)))

    def removeNestings(l):
        for i in l:
            if type(i) == list:
                removeNestings(i)
            else:
                timestamps.append(i)
    timestamps = []
    removeNestings(timestamps_initial)

    def wit_file(file, i):
        #time.sleep(1)
        start = time.time()
        try:
            with open("cache/" + file, 'rb') as f:
                resp = client.speech(f, {'Content-Type': 'audio/mpeg3'})
            os.remove("cache/" + file)
            if time.time() - start < 1:
                time.sleep(1 - (time.time() - start))
            if not "text" in resp:
                return "Error2345" + str(resp) + "\n"
            text = ""
            if file.count("_") == 1:
                ms = sum(timestamps[:i])
                text += str(int(ms/60000)).zfill(2) + ":" + str(int((ms%60000)/1000)).zfill(2) + "\n"
            text += resp["text"] + "\n"
            print(text)
            return text
        except Exception as e:
            os.remove("cache/" + file)
            return "Error2345" + str(e) + "\n"

    # for i, file in enumerate(tqdm(sorted(os.listdir("cache")))):
    #     text.append(wit_file(file))
    files = [file for file in sorted(os.listdir("cache")) if file.endswith('.mp3')]
    text = Parallel(n_jobs=1)(delayed(wit_file)(file, i) for i, file in enumerate(tqdm(files)))

    print(len([str for str in text if "Error2345" in str]))

    output = open("output/" + input + ".txt","a")
    output.writelines(text)
    #output.writelines([str for str in text if not "Error2345" in str])
    output.close()
