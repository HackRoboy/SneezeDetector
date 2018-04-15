import collections

import sys
import os
import pyaudio as pyaudio
import librosa

DEVICE_INDEX = 0
FORMAT = pyaudio.paInt16
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

        print('#')

        # ring buffer is full
        # if ring_buffer_chunknum == NUM_PADDING_CHUNKS:
        #     sys.stdout.write('-')
        #     sys.stdout.write('\n')
        #     # moving the full ring buffer to data (?)
        #     data = b''.join(ring_buffer)
        #     ### now we can try to find if it is about sneezing or not: ring_buffer (hajer part)
        #     print(
        #         hwDet.isHotword(
        #             data))  ### totally not sure how it works, but it doesnt accept current string - natalia
        #     ###
        #     ring_buffer.clear()
        #     ring_buffer_chunknum = 0

    stream.stop_stream()
    print("* done recording")

    stream.close()