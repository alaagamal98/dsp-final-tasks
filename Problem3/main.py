from scipy.io.wavfile import write
import wave  
import numpy as np
from choose import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
from Guitar import Ui_MainWindow as Ui_MainWindow1
from piano import Ui_MainWindow as Ui_MainWindow2

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.Guitar = Ui_MainWindow1()
        self.piano = Ui_MainWindow2()
        self.GuitarWindow = QtWidgets.QMainWindow()
        self.pianoWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self)
        self.Guitar.setupUi(self.GuitarWindow)  
        self.piano.setupUi(self.pianoWindow)  

        self.sample_rate = 44100
       
        self.frequancies =[{'C6':1046.50},{'B5':987.767},{'B5_A5':932.328},{'A5': 880},{'A5_G5':830.609},{'G5':783.991},{'G5_F5': 739.991},{'F5':698.456},{'E5':659.255},{'D5_E5': 622.254},
        {'D5':587.330},{'C5_D5':554.365},{'C5':523.251},{'B4':493.883},{'A4_B4':466.164},{'A4':440},{'G4_A4':415.305},{'G4':391.995},{'F4_G4':369.994},{'F4':349.228}]
      
        self.pianoButtons = [self.piano.C6_2,self.piano.B5_2,self.piano.B5_A5,self.piano.A5,self.piano.A5_G5,self.piano.G5,self.piano.G5_F5,self.piano.F5,self.piano.E5,self.piano.D5_E5,
                                self.piano.D5,self.piano.C5_D5,self.piano.C5,self.piano.B4,self.piano.A4_B4,self.piano.A4,self.piano.A4_G4,self.piano.G4,self.piano.F4_G4,self.piano.F4]
      
        self.Guitarfrequancies=[{'E':[82.41,87.31,92.50,92.50,98.00,103.83,110.00,116.54,123.47,130.81,138.59,146.83,155.56,164.81]},
                                {'B':[246.94,261.63,277.18,293.66,311.13,329.63,349.23,369.99,392.00,415.30,440.00,466.16,493.88]},
                                {'G': [196,207.65,220.00,233.08,246.94,261.63,277.18,293.66,293.66,311.13,329.63,349.23,369.99,392.00] },
                                {'D':[146.83,155.56,164.81,174.61,185,196,207.65,220.00,233.08,246.94,261.63,277.18,293.66]},
                                {'A':[110.00,116.54,123.47,130.81,138.59,146.83,155.56,164.81,174.81,174.61,185.00,196.00,207.65,220.00]},                               
                                {'E`':[329.63,349.23,369.99,392.00,415.30,440.00,466.16,493.88,523.25,554.37,587.33,622.25,659.26]}]
        self.PianoConnect=[lambda:self.soundPiano(0),lambda:self.soundPiano(1),lambda:self.soundPiano(2),lambda:self.soundPiano(3),
        lambda:self.soundPiano(4),lambda:self.soundPiano(5),lambda:self.soundPiano(6),lambda:self.soundPiano(7)
        ,lambda:self.soundPiano(8),lambda:self.soundPiano(9),lambda:self.soundPiano(10),lambda:self.soundPiano(11),lambda:self.soundPiano(12),
        lambda:self.soundPiano(13),lambda:self.soundPiano(14)
        ,lambda:self.soundPiano(15),lambda:self.soundPiano(16),lambda:self.soundPiano(17),lambda:self.soundPiano(18),lambda:self.soundPiano(19)]
        self.flagPiano = False
    
        self.ui.piano.clicked.connect(self.pianoShow)

        self.ui.guitar.clicked.connect(self.guitar)
    
    def pianoShow(self):
        
        self.pianoWindow.show()

        if (self.flagPiano == False):
            self.flagPiano = True
            for i in range (len(self.pianoButtons)):
                self.pianoButtons[i].clicked.connect(self.PianoConnect[i])    

    
    def PianoData(self,duration, freq,volume=1):
       
        t = np.linspace(0, duration, int(duration * self.sample_rate), False)
        audio = np.sin((freq*2*np.pi) * t)

        return(audio)
    
    def soundPiano(self,pianoBtn):
        
        for key, value in self.frequancies[pianoBtn].items():
            data = self.PianoData(1,value)
            scaled = np.int16(data/np.max(np.abs(data)) * 32767)
            self.playSound(scaled,pyaudio.paInt16)
                

    def guitar(self):
       self.GuitarWindow.show()
       self.Guitar.comboBox_2.activated.connect(self.guitarData)
       self.Guitar.comboBox.activated.connect(self.guitarData)
       
       

    def guitarData(self):

        freq = None
        for j in range (len(self.Guitarfrequancies)):
            for key,value in self.Guitarfrequancies[j].items():
                    if (key == str(self.Guitar.comboBox.currentText())):
                        freq = value[self.Guitar.comboBox_2.currentIndex()]
                        
               
        unit_delay = self.sample_rate//30
      
        stretch_factor = 2  
       
        guitar_sound=[]
        string = GuitarString(freq, unit_delay, self.sample_rate, stretch_factor)
       
        guitar_sound = np.array([string.get_sample() for _ in range(self.sample_rate* 3)],dtype=np.float32)
    
        self.playSound(guitar_sound,pyaudio.paFloat32)
      


   
    def playSound(self,data,soundFormat):
        
        p = pyaudio.PyAudio()

        stream = p.open(format=soundFormat,
                channels=1,
                rate=self.sample_rate,
                output=True)
        stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()


        
        
        
        


class GuitarString:
    def __init__(self, pitch, starting_sample, sampling_freq, stretch_factor):
        """Inits the guitar string."""
        self.pitch = pitch
        self.starting_sample = starting_sample
        self.sampling_freq = sampling_freq
        self.stretch_factor = stretch_factor
        self.init_wavetable()
        self.current_sample = 0
        self.previous_value = 0
        
    def init_wavetable(self):
        """Generates a new wavetable for the string."""
        wavetable_size = self.sampling_freq // int(self.pitch)
        self.wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
       
        
    def get_sample(self):
        """Returns next sample from string."""
        if self.current_sample >= self.starting_sample:
            current_sample_mod = self.current_sample % self.wavetable.size
            r = np.random.binomial(1, 1 - 1/self.stretch_factor)
            if r == 0:
                self.wavetable[current_sample_mod] =  0.5 * (self.wavetable[current_sample_mod] + self.previous_value)
            sample = self.wavetable[current_sample_mod]
            self.previous_value = sample
            self.current_sample += 1
        else:
            self.current_sample += 1
            sample = 0
        return sample



def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()