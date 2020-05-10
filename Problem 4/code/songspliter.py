from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import librosa

from scipy.io import wavfile
from pydub import AudioSegment


import librosa.display
# sr, y = wavfile.read("sweetbutpsycho.wav")
# if(len(y.shape)==2):
#     if(y.shape[1]==2):
#         y = np.mean(y, axis=1) 
# sound = AudioSegment.from_mp3("Amrdiab_wahshteny_17.mp3")
# sound.export("wavFile1" , format="wav")
y, sr = librosa.load('sweetbutpsycho.wav')
print(y)
print(sr)


# And compute the spectrogram magnitude and phase
S_full, phase = librosa.magphase(librosa.stft(y))
S_filter = librosa.decompose.nn_filter(S_full,
                                       aggregate=np.median,
                                       metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr)))

# The output of the filter shouldn't be greater than the input
# if we assume signals are additive.  Taking the pointwise minimium
# with the input spectrum forces this.
S_filter = np.minimum(S_full, S_filter)
margin_i, margin_v = 2, 10
power = 2

mask_i = librosa.util.softmask(S_filter,
                               margin_i * (S_full - S_filter),
                               power=power)

mask_v = librosa.util.softmask(S_full - S_filter,
                               margin_v * S_filter,
                               power=power)

# Once we have the masks, simply multiply them with the input spectrum
# to separate the components

S_foreground = mask_v * S_full
S_background = mask_i * S_full


back = librosa.istft(S_background)
fore = librosa.istft(S_foreground)


back_last= np.array(back,dtype= np.float64)
fore_last= np.array(fore,dtype= np.float64)
print("background")
print(back_last)
print("foreground")
print(fore_last)
librosa.output.write_wav('out1.wav',back_last,sr)
librosa.output.write_wav('out2.wav',fore_last,sr)
# wavfile.write('out1.wav', sr, back_last)
# wavfile.write('out2.wav', sr, fore_last)  