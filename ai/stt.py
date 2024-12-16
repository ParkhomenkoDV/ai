import sys
import json

import vosk
import sounddevice as sd
import queue

q = queue.Queue()

def q_callback(indata, frames, time, status):
    if status: print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback, samplerate: int, device: int):
    model = vosk.Model("RUSSIAN_small")
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
            # else:
            #    print(rec.PartialResult())


if __name__ == '__main__':
    model = vosk.Model("RUSSIAN_small")
    samplerate = 16000
    device = 1

    q = queue.Queue()
