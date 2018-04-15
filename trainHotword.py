import os
import librosa



def get_training_mfccs():
    if not (os.path.exists('./train_audio')):
        os.mkdir('./train_audio')

    trainDir = "./train_audio/"
    filelist = [f for f in os.listdir(trainDir) if f.endswith(".wav")]
    print("Hotword samples...")
    print(filelist)

    mfccs = []

    for f in filelist:
        y, sr = librosa.load(trainDir + f)
        mfcc = librosa.feature.mfcc(y, sr, n_mfcc=13)
        mfccs.append(mfcc.T)

    return mfccs
