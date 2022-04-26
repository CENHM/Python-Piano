import os
import time
import pyaudio
import wave
import threading


#在这里编谱
MusicList = {
    ("A+2", 0.000),
    ("A+0", 2.000), ("c-2", 2.000), ("e-2", 2.000),
    ("a-0", 2.500), ("c-1", 2.500), ("e-1", 2.500),
    ("a-0", 3.000), ("c-1", 3.000), ("e-1", 3.000),
    ("E+0", 3.500), ("b-1", 3.500), ("g-2", 3.500),
    ("b-0", 4.000), ("e-1", 4.000), ("g-0", 4.000),
    ("b-0", 4.500), ("e-1", 4.500), ("g-0", 4.500),
    ("A+0", 5.000), ("c-2", 5.000), ("e-2", 5.000),
    ("a-0", 5.500), ("c-1", 5.500), ("e-1", 5.500),
    ("a-0", 6.000), ("c-1", 6.000), ("e-1", 6.000),
    ("E+0", 6.500), ("b-1", 6.500), ("g-2", 6.500),
    ("b-0", 7.000), ("e-1", 7.000), ("g-0", 7.000),
    ("b-0", 7.500), ("e-1", 7.500), ("g-0", 7.500),
    ("A+0", 8.000), ("c-2", 8.000), ("e-2", 8.000),
    ("a-0", 8.500), ("c-1", 8.500), ("e-1", 8.500),
    ("a-0", 9.000), ("c-1", 9.000), ("e-1", 9.000),
    ("E+0", 9.500), ("b-1", 9.500), ("g-2", 9.500),
    ("b-0", 10.00), ("e-1", 10.00), ("g-0", 10.00),
    ("b-0", 10.50), ("e-1", 10.50), ("g-0", 10.50),
    ("F+0", 11.00), ("c-2", 11.00), ("e-2", 11.00),
    ("f-0", 11.50), ("a-0", 11.50), ("c-1", 11.50),
    ("f-0", 12.00), ("a-0", 12.00), ("c-1", 12.00),
    ("d-0", 12.50), ("b-1", 12.50), ("g-2", 12.50),
    ("a-0", 13.00), ("d-1", 13.00), ("f-1", 13.00),

    ("c-0", 13.50), ("B+0", 13.75), ("B+0", 14.00), ("A+0", 14.00),
    ("a-1", 14.25), ("g-#1",14.50),
    ("a-1", 14.75), ("a-0", 14.75), ("c-1", 14.75), ("e-1", 14.75),
    ("b-1", 15.00),
    ("c-2", 15.25), ("a-0", 15.25), ("c-1", 15.25), ("e-1", 15.25),
    ("d-2", 15.50),
    ("e-2", 15.75), ("E+0", 15.75),
    ("g-2", 16.00),
    ("e-2", 16.25), ("g-0", 16.25), ("b-0", 16.25), ("e-1", 16.25),
    ("a-2", 16.50),
    ("e-2", 16.75), ("g-0", 16.75), ("b-0", 16.75), ("e-1", 16.75),
    ("d-2", 17.25), ("c-0", 17.25),
    ("e-2", 17.50),
    ("c-2", 17.75), ("g-0", 17.75), ("c-1", 17.75), ("e-1", 17.75),
    ("d-2", 18.00),
    ("b-1", 18.25), ("g-0", 18.25), ("c-1", 18.25), ("e-1", 18.25),
    ("c-2", 18.50),
    ("a-1", 18.75), ("G+0", 18.75),
    ("g-0", 19.25), ("b-0", 19.25), ("d-1", 19.25),
    ("g-1", 19.50),
    ("g-0", 19.75), ("b-0", 19.75), ("d-1", 19.75),

    ("A+0", 20.25), ("c-2", 20.25), ("e-2", 20.25),
    ("a-0", 20.75), ("c-1", 20.75), ("e-1", 20.75),
    ("a-0", 21.25), ("c-1", 21.25), ("e-1", 21.25),
    ("E+0", 21.75), ("b-1", 21.75), ("g-2", 21.75),
    ("b-0", 22.25), ("e-1", 22.25), ("g-0", 22.25),
    ("b-0", 22.75), ("e-1", 22.75), ("g-0", 22.75),
    ("A+0", 23.25), ("c-2", 23.25), ("e-2", 23.25),
    ("a-0", 23.75), ("c-1", 23.75), ("e-1", 23.75),
    ("a-0", 24.25), ("c-1", 24.25), ("e-1", 24.25),
    ("E+0", 24.75), ("b-1", 24.75), ("g-2", 24.75),
    ("b-0", 25.25), ("e-1", 25.25), ("g-0", 25.25),
    ("b-0", 25.75), ("e-1", 25.75), ("g-0", 25.75),
    ("A+0", 26.25), ("c-2", 26.25), ("e-2", 26.25),
    ("a-0", 26.75), ("c-1", 26.75), ("e-1", 26.75),
    ("a-0", 27.25), ("c-1", 27.25), ("e-1", 27.25),
    ("E+0", 27.75), ("b-1", 27.75), ("g-2", 27.75),
    ("b-0", 28.25), ("e-1", 28.25), ("g-0", 28.25),
    ("b-0", 28.75), ("e-1", 28.75), ("g-0", 28.75),
    ("F+0", 29.25), ("c-2", 29.25), ("e-2", 29.25),
    ("f-0", 29.75), ("a-0", 29.75), ("c-1", 29.75),
    ("f-0", 30.25), ("a-0", 30.25), ("c-1", 30.25),
    ("d-0", 30.75), ("b-1", 30.75), ("g-2", 30.75),
    ("a-0", 31.25), ("d-1", 31.25), ("f-1", 31.25),
    ("a-0", 31.75), ("d-1", 31.75), ("f-1", 31.75),

    ("a-1", 32.25), ("A+0", 32.25), ("g-#1", 32.50),
    ("a-1", 32.75), ("a-0", 32.75), ("c-1", 32.75), ("e-1", 32.75),
    ("b-1", 33.00),
    ("c-2", 33.25), ("a-0", 33.25), ("c-1", 33.25), ("e-1", 33.25),
    ("d-2", 33.50),
    ("e-2", 33.75), ("E+0", 33.75),
    ("g-2", 34.00),
    ("a-2", 34.25), ("g-0", 34.25), ("b-0", 34.25), ("e-1", 34.25),
    ("e-2", 34.50),
    ("g-2", 34.75), ("g-0", 34.75), ("b-0", 34.75), ("e-1", 34.75),
    ("d-2", 35.00),
    ("e-2", 35.25), ("F+0", 35.25),
    ("c-2", 35.50),
    ("d-2", 35.75), ("f-0", 35.75), ("a-0", 35.75), ("c-1", 35.75),
    ("b-1", 36.00),
    ("c-2", 36.25), ("f-0", 36.25), ("a-0", 36.25), ("c-1", 36.25),
    ("a-1", 36.50),
    ("b-1", 36.75), ("d-0", 36.75),
    ("g-1", 37.00),
    ("a-1", 37.25), ("a-0", 37.25),("d-1", 37.25),("f-1", 37.25),
    ("c-0", 37.75), ("B+0", 38.00),

    ("A+0", 38.25), ("c-2", 38.25), ("e-2", 38.25),
    ("a-0", 38.75), ("c-1", 38.75), ("e-1", 38.75),
    ("a-0", 39.25), ("c-1", 39.25), ("e-1", 39.25),
    ("E+0", 39.75), ("b-1", 39.75), ("g-2", 39.75),
    ("g-0", 40.25), ("b-0", 40.25), ("e-1", 40.25),
    ("g-0", 40.75), ("b-0", 40.75), ("e-1", 40.75),
    ("c-0", 41.25), ("c-2", 41.25), ("e-2", 41.25),
    ("g-0", 41.75), ("c-1", 41.75), ("e-1", 41.75),
    ("g-0", 42.25), ("c-1", 42.25), ("e-1", 42.25),
    ("G+0", 42.75), ("b-1", 42.75), ("g-2", 42.75),
    ("g-0", 43.25), ("b-0", 43.25), ("d-1", 43.25),
    ("g-0", 43.75), ("b-0", 43.75), ("d-1", 43.75),
    ("G+#0",44.00),
    ("A+0", 44.25), ("c-2", 44.25), ("e-2", 44.25),
    ("a-0", 44.75), ("c-1", 44.75), ("e-1", 44.75),
    ("a-0", 45.25), ("c-1", 45.25), ("e-1", 45.25),
    ("E+0", 45.75), ("b-1", 45.75), ("g-2", 45.75),
    ("g-0", 46.25), ("b-0", 46.25), ("e-1", 46.25),
    ("g-0", 46.75), ("b-0", 46.75), ("e-1", 46.75),
    ("F+0", 47.25), ("c-2", 47.25), ("e-2", 47.25),
    ("c-1", 47.75), ("f-1", 47.75), ("a-1", 47.75),
    ("c-1", 48.25), ("f-1", 48.25), ("a-1", 48.25),
    ("d-0", 48.75), ("b-1", 48.75), ("g-2", 48.75),
    ("a-0", 49.25), ("d-1", 49.25), ("f-1", 49.25),

    ("c-0", 49.75), ("B+0", 50.00),
    ("A+0", 50.25), ("a-1", 50.25),
    ("g-#1",50.50),
    ("a-1", 50.75), ("a-0", 50.75), ("c-1", 50.75),
    ("b-1", 51.00),
    ("c-2", 51.25), ("a-0", 51.25), ("c-1", 51.25),
    ("d-2", 51.50),
    ("e-2", 51.75), ("E+0", 51.75),
    ("g-2", 52.00),
    ("e-2", 52.25), ("g-0", 52.25), ("b-0", 52.25),
    ("a-2", 52.50),
    ("e-2", 52.75), ("g-0", 52.75), ("b-0", 52.75),
    ("d-2", 53.25), ("F+0", 53.25),
    ("e-2", 53.50),
    ("c-2", 53.75), ("f-0", 53.75), ("a-0", 53.75),
    ("d-2", 54.00),
    ("b-1", 54.25), ("f-0", 54.25), ("a-0", 54.25),
    ("c-2", 54.50),
    ("a-1", 54.75), ("d-0", 54.75),
    ("a-0", 55.25), ("d-1", 55.25), ("f-1", 55.25),
    ("g-1", 55.40),
    ("c-0", 55.75), ("B+0", 55.75),

    ("A+0", 56.00), ("a-1", 56.00), ("c-2", 56.00), ("e-2", 56.00),
    ("a-0", 56.50), ("c-1", 56.50), ("e-1", 56.50),
    ("a-0", 57.00), ("c-1", 57.00), ("e-1", 57.00),
    ("E+0", 57.50), ("b-1", 57.50), ("g-2", 57.50),
    ("b-0", 58.00), ("e-1", 58.00), ("g-0", 58.00),
    ("b-0", 58.50), ("e-1", 58.50), ("g-0", 58.50),
    ("A+0", 59.00), ("c-2", 59.00), ("e-2", 59.00),
    ("a-0", 59.50), ("c-1", 59.50), ("e-1", 59.50),
    ("E+0", 60.50), ("b-1", 60.50), ("g-2", 60.50),
    ("a-0", 61.00), ("e-1", 61.00), ("g-0", 61.00),
    ("c-2", 62.00), ("e-2", 62.00),
    ("a-0", 62.50), ("c-1", 62.50), ("e-1", 62.50),
    ("E+0", 63.50), ("b-1", 63.50), ("g-2", 63.50),
    ("a-0", 64.00), ("e-1", 64.00), ("g-0", 64.00),
    ("A+0", 65.25), ("a-2", 65.25), ("c-2", 65.25), ("e-2", 65.25),
}

filepath = os.path.dirname(__file__)


def playWAV(title, pause):
    time.sleep(pause)
    path = filepath + '/keys/' + title + '.wav'
    chunk = 1024
    file = wave.open(path, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(file.getsampwidth()),
                    channels=file.getnchannels(),
                    rate=file.getframerate(),
                    output=True)
    data = file.readframes(chunk)

    while len(data) > 0:
        stream.write(data)
        data = file.readframes(chunk)


def play():
    threads = []
    for music in MusicList:
        t = threading.Thread(target=playWAV, args=(music[0], music[1]))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("There will be blood.")
    play()
