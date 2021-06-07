from dtw import dtw
import io
import matplotlib.pyplot as plt
import numpy as np
import librosa
import copy
import os


class AudioAnalysis:
    FULL_SENTENCE = 'kurang jelas terhadap sistem pengagihan bonus dalam kalangan pegawai jabatan menjadi punca kepada kejadian mogok dan tindakan melempar barangan milik pelanggan oleh kakitangan J&T Express'
    SAMPLE_WORDS = FULL_SENTENCE.split()
    PARENT_FOLDER = r'core\storage'
    FULL_TARGET_FOLDER = 'full'
    SAMPLE_FOLDER_1 = 'sample 1'
    SAMPLE_FOLDER_2 = 'sample 2'
    GRAPH_FOLDER_1 = 'graph 1'
    GRAPH_FOLDER_2 = 'graph 2'
    DETECTED_FOLDER_1 = 'detected 1'
    DETECTED_FOLDER_2 = 'detected 2'
    AUDIO_SAMPLE_1 = []
    AUDIO_SAMPLE_2 = []
    TARGET_FULL_AUDIO = None
    TARGET_FULL_RATE = None

    def __init__(self) -> None:
        self.mfcc_samples_1 = []
        self.mfcc_samples_2 = []
        self.target_full_mfcc = None

        parent_path = r'core\storage'

        for i, word in enumerate(self.__class__.SAMPLE_WORDS):
            full_name = f'{i+1}_{word}.mp3'
            # Samples 1
            audio_1, rate_1 = librosa.load(os.path.join(parent_path,
                                                        self.__class__.SAMPLE_FOLDER_1,
                                                        full_name))
            self.mfcc_samples_1.append((audio_1, rate_1))
            # Samples 2
            audio_2, rate_2 = librosa.load(os.path.join(parent_path,
                                                        self.__class__.SAMPLE_FOLDER_2,
                                                        full_name))
            self.mfcc_samples_2.append((audio_2, rate_2))

        target_audio_name = 'J&T Sistem Pengagihan Bonus Tak Jelas.mp3'
        self.target_full_audio, self.ftarget_full_rate = librosa.load(os.path.join(parent_path,
                                                                                   self.__class__.FULL_TARGET_FOLDER,
                                                                                   target_audio_name))

    def run_DTW(self, mfcc_samples: list, target_full_mfcc: 'np.ndarray'):
        # get window sizes for each audio samples
        window_sizes = np.array([int(mfcc_samples[i][0].shape[1]//1) for i in range(len(mfcc_samples))])
        # prepare 2d list for dtw
        dists_2d = []
        for i in range(len(mfcc_samples)):
            dists_2d.append(np.zeros(target_full_mfcc.shape[1] - window_sizes[i]))

        # dtw
        # for each words
        for i in range(len(mfcc_samples.shape[0])):
            # for each interval
            for j in range(len(dists_2d[i])):
                part_target_mfcc = target_full_mfcc[:, j:j+window_sizes[i]]
                single_dist = dtw(part_target_mfcc.T, mfcc_samples[i][0].T, dist=lambda x, y: np.linalg.norm(x - y))[0]
                dists_2d[i][j] = single_dist

    def get_timeRange(dists: list, window_size: int):
        '''Get time range from mfcc'''
        # smallest value index
        word_match_idx = dists.argmin()
        # get index bounds
        word_match_idx_bnds = np.array([word_match_idx, np.ceil(word_match_idx+window_size)])
        samples_per_mfcc = 512
        # get time bounds
        word_samp_bounds = word_match_idx_bnds*samples_per_mfcc
        return (int(word_samp_bounds[0]), int(word_samp_bounds[1]))

    @classmethod
    def preprocess_mfcc(cls, mfcc: 'np.ndarray'):
        '''Normalize mfcc to increase accuracy'''
        mfcc_cp = copy.deepcopy(mfcc)
        for i in range(mfcc.shape[1]):
            mfcc_cp[:, i] = mfcc[:, i] - np.mean(mfcc[:, i])
            mfcc_cp[:, i] = mfcc_cp[:, i]/np.max(np.abs(mfcc_cp[:, i]))
        return mfcc_cp

    @classmethod
    def generate_mfccs(cls, audio_samples: 'np.ndarray'):
        '''Convert audio to mfccs'''
        mfcc_samples = []
        for i, (sample_audio, sample_rate) in enumerate(audio_samples):
            x_mfcc = librosa.feature.mfcc(sample_audio, sample_rate)
            x_mfcc = cls.preprocess_mfcc(x_mfcc)
            mfcc_samples.append((x_mfcc, sample_rate))
        return mfcc_samples
