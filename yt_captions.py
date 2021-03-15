from pytube import YouTube

file = open('input.txt', 'r')
Lines = file.readlines()

for url in Lines:
    yt = YouTube(url)
    if len(yt.captions.all()) == 0:
        print("No captions found for: " + url)
    for i, caption in enumerate(yt.captions.all()):
        print(i)
        caption.download(url.split("?v=")[1] + str(i))
