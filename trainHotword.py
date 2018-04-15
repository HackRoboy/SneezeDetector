import os
import librosa



def get_training_mfccs():
    if not (os.path.exists('./train_audio')):
        os.mkdir('./train_audio')

    filelist = [f for f in os.listdir("./train_audio/") if f.endswith(".wav")]
    print("Hotword samples...")
    print(filelist)

    mfccs = []

    for i in range(len(filelist)):
        y, sr = librosa.load('train_audio/{}.wav'.format(i))
        mfcc = librosa.feature.mfcc(y, sr, n_mfcc=13)
        mfccs.append(mfcc.T)
