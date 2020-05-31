from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
import sys
import numpy as np
import pandas as pd
from scipy.io import wavfile
from os import path
from pydub import AudioSegment
import os
import scipy
from sklearn.decomposition import FastICA
import librosa


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data =[]
        self.firstSongToSplit = 1
        self.firstTime = 0
        self.ui.opensong.clicked.connect(self.getfile)
        self.ui.splitsong.clicked.connect(self.splitSong)
        self.ui.cocktailparty.clicked.connect(self.CocktailPartyFile)
        self.ui.ecg.clicked.connect(self.ecgFile)

    def getfile(self):
        path, extention = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                "(*.mp3);;(*.csv);;(*.wav) ")
        self.head, self.filename = os.path.split(path)
        self.wavFile = self.head+'/'+self.filename[:-4] + '.wav'
        if(path != ''):
            self.read_file(path, extention)
        else:
            pass

    def read_file(self, path, ext):
        if ext == "(*.mp3)":
            sound = AudioSegment.from_mp3(path)
            sound.export(self.wavFile, format="wav")
            self.samplerate, self.data = wavfile.read(self.wavFile)
        elif ext == "(*.wav)":
            self.samplerate, self.data = wavfile.read(path)
        
    def splitSong(self):
        if  len(self.data)==0:
            pass
        else :
            # librosa
            if self.firstSongToSplit == 0 :
                self.ui.original.plot(clear = True)
                self.ui.comp1.plot (clear = True)
                self.ui.comp2.plot(clear = True)
            elif self.firstSongToSplit == 1:
                self.firstSongToSplit = 0  
            if(self.data.shape[1]>=2):
                plotting_data = np.mean(self.data, axis=1) 
            S_full,phase = librosa.magphase(librosa.stft(plotting_data))
            S_filter = librosa.decompose.nn_filter(S_full,
                                           aggregate=np.median,
                                           metric='cosine',
                                           width=int(librosa.time_to_frames(2, sr=self.samplerate)))
            S_filter = np.minimum(S_full, S_filter)
            margin_i, margin_v = 2, 10
            power = 2
            mask_i = librosa.util.softmask(S_filter,
                                   margin_i * (S_full - S_filter),
                                   power=power)
            mask_v = librosa.util.softmask(S_full - S_filter,
                                   margin_v * S_filter,
                                   power=power)
            S_foreground = mask_v * S_full
            S_background = mask_i * S_full
            back = librosa.istft(S_background)
            fore = librosa.istft(S_foreground)
            back_last= np.array(back,dtype= np.int16)
            fore_last= np.array(fore,dtype= np.int16)
            plotting_data /= abs(plotting_data).max(axis = 0)
            back /= abs(back).max(axis = 0)
            fore /= abs(fore).max(axis = 0)
            self.ui.songdata.plot( plotting_data, pen='g')
            self.ui.sep1.plot(back, pen='b')
            self.ui.sep2.plot( fore, pen='r')
            wavfile.write('SeparatedSong1.wav', self.samplerate, back_last)
            wavfile.write('SeparatedSong2.wav', self.samplerate, fore_last)
          

    def CocktailPartyFile(self):
        if self.firstTime == 1 :
            self.ui.original.plot(clear = True)
            self.ui.comp1.plot (clear = True)
            self.ui.comp2.plot(clear = True)
            self.ui.comp3.plot(clear = True)
        elif self.firstTime == 0:
            self.firstTime = 1     
        sr , data = wavfile.read("Data/CocktailParty.wav")
        ica = FastICA(n_components=4)
        ica.fit(data)
        S_ = ica.transform(data)
        if(data.shape[1] >= 2):
            original_data = np.mean(data, axis=1)
        
        S_[:, 0] /= abs(S_[:, 0]).max(axis=0)
        S_[:, 1] /= abs(S_[:, 1]).max(axis=0)
        S_[:, 2] /= abs(S_[:, 2]).max(axis=0)
        S_[:, 3] /= abs(S_[:, 3]).max(axis=0)
        wavfile.write("CocktailSource1.wav",sr,S_[:, 0])
        wavfile.write("CocktailSource2.wav",sr,S_[:, 1])
        wavfile.write("CocktailSource3.wav",sr,S_[:, 2])
        wavfile.write("CocktailSource4.wav",sr,S_[:, 3])
        transpose = np.transpose(S_)
        sample_length = transpose[0].shape[0]
        time = np.arange(sample_length) / sr
        self.ui.original.plot(time,original_data, pen='y')
        self.ui.comp1.plot(time, S_[:, 0], pen='r')
        self.ui.comp2.plot(time,S_[:, 1], pen='b')
        self.ui.comp3.plot(time, S_[:, 2], pen='g')

    def ecgFile(self):
        if self.firstTime == 1 :
            self.ui.original.plot(clear = True)
            self.ui.comp1.plot (clear = True)
            self.ui.comp2.plot(clear = True)
            self.ui.comp3.plot(clear = True)
        elif self.firstTime == 0:
            self.firstTime = 1 
        data = pd.read_csv("Data/ECG.csv")
        data = data.iloc[0:1000,1:3] 
        ica = FastICA(n_components=2)
        ica.fit(data)
        S_ = ica.transform(data)   
        if(data.shape[1] >= 2):
            original_data = np.mean(data, axis=1)
        self.ui.original.plot(original_data, pen='y')
        self.ui.comp1.plot(S_[:, 0], pen='r')
        self.ui.comp2.plot(S_[:, 1], pen='b')

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()


