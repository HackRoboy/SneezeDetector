import sys
import os
import librosa

if not (os.path.exists('./train_audio')):
	os.mkdir('./train_audio')
sys.path.append(os.path.abspath('./hotword_detection'))
import wordRecorder as wr
import time

wRec = wr.wordRecorder()
filelist = [ f for f in os.listdir("./train_audio/") if f.endswith(".wav") ]
print(filelist)
print("Record hotword instances...")

mfccs = {}

for i in range(len(filelist)):
    y, sr = librosa.load('train_audio/{}.wav'.format(i))
    mfcc = librosa.feature.mfcc(y, sr, n_mfcc=13)
    mfccs[i] = mfcc.T