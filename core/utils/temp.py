from dtw import dtw
import numpy as np
import librosa
import matplotlib.pyplot as plt
import os

def word_spoken_DTW(target_mfcc, mfcc_sample, window_size:int):
    new_dist = np.zeros(target_mfcc.shape[1] - window_size)
    for j in range(target_mfcc.shape[1] - window_size): 
        part_target_mfcc = target_mfcc[:,j:j+window_size]
        single_dist = dtw(part_target_mfcc.T, mfcc_sample.T, dist=lambda x, y: np.linalg.norm(x - y))[0]
        new_dist[j] = single_dist
    return new_dist