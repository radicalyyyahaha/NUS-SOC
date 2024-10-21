import sounddevice as sd
import queue
import vosk
import json
import sys
import main

q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


model = vosk.Model("vosk-model-small-en-us-0.15")

samplerate = 16000
device = None

keyword1 = "hi"
keyword2 = "wrong"
keyword3 = "play"

count1 = 0
count2 = 0
count3 = 0


with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                       channels=1, callback=callback):
    print('#' * 80)
    print('Press Ctrl+C to stop the recording')
    print('#' * 80)

    rec = vosk.KaldiRecognizer(model, samplerate)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get('text', '')
            print(f"Recognized: {text}")
            if keyword1 in text:
                main.hello()
            elif keyword2 in text or 'around' in text:
                main.rotate()
            elif keyword3 in text:
                main.play_ball()

        else:
            partial_result = rec.PartialResult()
            partial_text = json.loads(partial_result).get('partial', '')
            print(f"Partial: {partial_text}")
            if keyword1 in partial_text:
                count1 += 1
                if count1 > 5:
                    main.hello()
                    count1 = 0
            elif keyword2 in partial_text or 'around' in partial_text:
                count2 += 1
                if count2 > 5:
                    count2 = 0
                    main.rotate()
            elif keyword3 in partial_text:
                count3 += 1
                if count3 > 5:
                    count3 = 0
                    main.play_ball()
