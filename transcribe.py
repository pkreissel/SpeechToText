from wit import Wit
from pydub import AudioSegment
from pydub.silence import split_on_silence
from joblib import Parallel, delayed
from tqdm import tqdm
import os
from keys import WIT_KEY
import time
import sys

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
            for i, subchunk in enumerate(subchunks):
                chunkexport(subchunk, num + "_" + str(i).zfill(3), level + 1)
        else:
            try:
                chunk.export("cache/chunk{0}.mp3".format(num), format="mp3")
            except Exception as e:
                print(e)

    print("second split round, this will run in parallel")
    Parallel(n_jobs=12)(delayed(chunkexport)(chunk, str(i).zfill(3), 1) for i, chunk in enumerate(tqdm(chunks)))

    text = []

    def wit_file(file):
        #time.sleep(1)
        start = time.time()
        if not file.endswith('.mp3'):
            return "Error2345" + "\n"
        try:
            with open("cache/" + file, 'rb') as f:
                resp = client.speech(f, {'Content-Type': 'audio/mpeg3'})
            os.remove("cache/" + file)
            if time.time() - start < 1:
                time.sleep(1 - (time.time() - start))
            if not "text" in resp:
                return "Error2345" + str(resp) + "\n"
            return resp["text"] + "\n"
        except Exception as e:
            os.remove("cache/" + file)
            return "Error2345" + str(e) + "\n"

    # for i, file in enumerate(tqdm(sorted(os.listdir("cache")))):
    #     text.append(wit_file(file))
    text = Parallel(n_jobs=1)(delayed(wit_file)(file) for i, file in enumerate(tqdm(sorted(os.listdir("cache")))))

    print(len([str for str in text if "Error2345" in str]))

    output = open("output/" + input + ".txt","a")
    output.writelines(text)
    #output.writelines([str for str in text if not "Error2345" in str])
    output.close()
