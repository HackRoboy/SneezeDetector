import collections

import sys
import os
import numpy as np
import pyaudio as pyaudio
import librosa

from trainHotword import get_training_mfccs
import detectHotword

DEVICE_INDEX = 0
FORMAT = pyaudio.paFloat32
NPFORMAT = np.float32
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1000
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)


def get_mic_stream():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     start=False,
                     input_device_index=DEVICE_INDEX,
                     frames_per_buffer=CHUNK_SIZE)
    print('Streaming from Mic:')
    print(pa.get_device_info_by_index(DEVICE_INDEX))
    return stream



if __name__ == '__main__':

    print('Loading Samples')
    hotwordData = get_training_mfccs()
    print('Samples loaded')

    threshold = detectHotword.get_avg_distance_between_all(hotwordData)


    stream = get_mic_stream()

    leave = False

    ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
    ring_buffer_chunknum = 0
    buffer_in = ''

    print("* recording")
    stream.start_stream()

    while not leave:
        chunk = stream.read(CHUNK_SIZE)

        ring_buffer_chunknum += 1
        ring_buffer.append(chunk)

        print('#', end='', flush=True)

        # ring buffer is full
        if ring_buffer_chunknum == NUM_PADDING_CHUNKS:
            print()
            # moving the full ring buffer to data (?)
            data = np.fromstring(b''.join(ring_buffer), dtype=NPFORMAT)

            mfcc = librosa.feature.mfcc(data, RATE)
            if detectHotword.get_avg_distance(mfcc, hotwordData) < threshold:
                print('HOTWORD!')

            ring_buffer.clear()
            ring_buffer_chunknum = 0

    stream.stop_stream()
    print("* done recording")

    stream.close()