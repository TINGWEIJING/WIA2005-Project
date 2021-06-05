import pytube
import moviepy.editor as mp
from gtts import gTTS
from dtw import dtw
import io
import matplotlib.pyplot as plt
import numpy as np
import librosa
import IPython.display
from IPython.display import Image
import copy
import os

class AudioAnalysis:
    pass

    @classmethod
    def preprocess_mfcc(cls, mfcc):
        mfcc_cp = copy.deepcopy(mfcc)
        for i in range(mfcc.shape[1]):
            mfcc_cp[:,i] = mfcc[:,i] - np.mean(mfcc[:,i])
            mfcc_cp[:,i] = mfcc_cp[:,i]/np.max(np.abs(mfcc_cp[:,i]))
        return mfcc_cp
