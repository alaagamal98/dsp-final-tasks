from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
import sys
import numpy as np
from scipy.io import wavfile
from os import path
from pydub import AudioSegment
import os


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.getfile)
    def getfile(self):
        path,extention = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",
            "(*.mp3);;(*.wav) ")
        self.head,self.filename = os.path.split(path)
        self.wavFile = self.head+'/'+self.filename[:-4] + '.wav'
        if(path!=''):

            self.read_file(path) 

        else:
            pass 
    def read_file(self,path,i):
        sound = AudioSegment.from_mp3(path)
        sound.export(self.wavFile , format="wav")  
        self.samplerate, self.data[i] = wavfile.read(self.wavFile)
        if(len(self.data[i].shape)==2):
            if (self.data[i].shape[1]==2):
                self.data[i]  = np.mean(self.data[i], axis=1)
               


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()