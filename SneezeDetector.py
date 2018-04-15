#!/usr/bin/env python3
import struct
import wave

import collections

import sys
import os
import numpy as np
import pyaudio as pyaudio
import librosa

from trainHotword import get_training_mfccs
import detectHotword
from play_bless import play_bless

DEVICE_INDEX = 0
FORMAT = pyaudio.paFloat32
NPFORMAT = np.float32
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 5000
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)

pa = pyaudio.PyAudio()


def get_mic_stream():
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


# see http://stackoverflow.com/questions/15576798/create-32bit-float-wav-file-in-python
# see... http://blog.theroyweb.com/extracting-wav-file-header-information-using-a-python-script
def float32_wav_file(file_name, sample_array, sample_rate):
    sample_array = np.atleast_2d(sample_array)
    (M, N) = sample_array.shape
    print ("len sample_array=(%d,%d)" % (M,N))
    byte_count = M * N * 4  # (len(sample_array)) * 4  # 32-bit floats
    wav_file = b""
    # write the header
    wav_file += struct.pack('<ccccIccccccccIHHIIHH',
                            b'R', b'I', b'F', b'F',
                            byte_count + 0x2c - 8,  # header size
                            b'W', b'A', b'V', b'E', b'f', b'm', b't', b' ',
                            0x10,  # size of 'fmt ' header
                            3,  # format 3 = floating-point PCM
                            M,  # channels
                            sample_rate,  # samples / second
                            sample_rate * 4,  # bytes / second
                            4,  # block alignment
                            32)  # bits / sample
    wav_file += struct.pack('<ccccI',
                            b'd', b'a', b't', b'a', byte_count)
    print("packing...")
    for j in range(0, N):
        for k in range(0, M):
            wav_file += struct.pack("<f", sample_array[k, j])
    print("saving...")
    fi = open(file_name, 'wb')
    fi.write(wav_file)
    fi.close()

    return wav_file


if __name__ == '__main__':

    print('Loading Samples')
    hotwordData = get_training_mfccs()
    print('Samples loaded')

    threshold = detectHotword.get_avg_distance_between_all(hotwordData)

    print('Threshold: %f' % threshold)

    # play_bless()

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
            d = b''.join(ring_buffer)
            data = np.fromstring(d, dtype=NPFORMAT)

            float32_wav_file('test.wav', data, RATE)
            exit(0)

            mfcc = librosa.feature.mfcc(data, RATE, n_mfcc=13)
            dist = detectHotword.get_avg_distance(mfcc.T, hotwordData)
            print('D: %f ' % dist, end='')
            if dist < threshold:
                print('HOTWORD!')
                play_bless()
            else:
                print('Nothing')

            ring_buffer.clear()
            ring_buffer_chunknum = 0

    stream.stop_stream()
    print("* done recording")

    stream.close()
