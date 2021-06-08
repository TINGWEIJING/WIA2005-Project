from dtw import dtw
import io
import matplotlib.pyplot as plt
import numpy as np
import librosa
import copy
import os
import shutil
import concurrent.futures
import time
import soundfile as sf
import json


class AudioAnalysis:
    # == Constants ==
    FULL_SENTENCE = 'kurang jelas terhadap sistem pengagihan bonus dalam kalangan pegawai jabatan menjadi punca kepada kejadian mogok dan tindakan melempar barangan milik pelanggan oleh kakitangan J&T Express'
    SAMPLE_WORDS = FULL_SENTENCE.split()
    TARGET_AUDIO_NAME = 'J&T Sistem Pengagihan Bonus Tak Jelas.mp3'
    TARGET_URL = r'https://youtu.be/OnAA1dIG6iY'
    PARENT_FOLDER = r'..\static'
    ALTER_PARENT_FOLDER = r'.\core\static'
    # == Folder Names ==
    FULL_TARGET_FOLDER = 'full'
    SAMPLE_FOLDER_1 = 'sample 1'
    SAMPLE_FOLDER_2 = 'sample 2'
    GRAPH_FOLDER_1 = 'graph 1'
    GRAPH_FOLDER_2 = 'graph 2'
    DETECTED_FOLDER_1 = 'detected 1'
    DETECTED_FOLDER_2 = 'detected 2'
    # == Librosa Audio ==
    AUDIO_SAMPLE_1 = []
    AUDIO_SAMPLE_2 = []
    TARGET_FULL_AUDIO = None
    TARGET_FULL_RATE = None
    # == MFCC ==
    MFCC_SAMPLE_1 = []
    MFCC_SAMPLE_2 = []
    TARGET_FULL_MFCC = None
    # == WINDOW ==
    WINDOW_SIZE_1 = []
    WINDOW_SIZE_2 = []
    # == DISTANCE 2D LISTS==
    DIST_2D_1 = []
    DIST_2D_2 = []
    # == TIME RANGES LIST ==
    TIME_RANGE_1 = []
    TIME_RANGE_2 = []
    # =========================

    def __init__(self) -> None:
        if not os.path.exists(self.__class__.PARENT_FOLDER):
            self.__class__.PARENT_FOLDER = self.__class__.ALTER_PARENT_FOLDER

    @classmethod
    def run_audio_analysis(cls):
        '''Rerun all the audio analysis'''
        start_time = time.time()
        plt.rcParams.update({'figure.max_open_warning': 0})
        # load all audio data
        # target audio
        target_paths = [os.path.join(cls.PARENT_FOLDER, cls.FULL_TARGET_FOLDER, cls.TARGET_AUDIO_NAME)]
        cls.TARGET_FULL_AUDIO, cls.TARGET_FULL_RATE = cls.load_multi_audio(target_paths)[0]
        # sample 1
        sample_1_paths = [os.path.join(cls.PARENT_FOLDER, cls.SAMPLE_FOLDER_1, f'{i+1}_{word}.mp3') for i, word in enumerate(cls.SAMPLE_WORDS)]
        cls.AUDIO_SAMPLE_1 = cls.load_multi_audio(sample_1_paths)
        # sample 2
        sample_2_paths = [os.path.join(cls.PARENT_FOLDER, cls.SAMPLE_FOLDER_2, f'{i+1}_{word}.mp3') for i, word in enumerate(cls.SAMPLE_WORDS)]
        cls.AUDIO_SAMPLE_2 = cls.load_multi_audio(sample_2_paths)
        print('Finish reading audio files:', (time.time() - start_time))

        # preprocess
        # target audio
        cls.TARGET_FULL_MFCC, _ = cls.convert_MFCC(cls.TARGET_FULL_AUDIO, cls.TARGET_FULL_RATE)
        # sample 1
        cls.MFCC_SAMPLE_1 = [cls.convert_MFCC(sample_audio, sample_rate) for (sample_audio, sample_rate) in cls.AUDIO_SAMPLE_1]
        # sample 2
        cls.MFCC_SAMPLE_2 = [cls.convert_MFCC(sample_audio, sample_rate) for (sample_audio, sample_rate) in cls.AUDIO_SAMPLE_2]
        print('Finish MFCC convertion:', (time.time() - start_time))

        # windows
        # sample 1
        cls.WINDOW_SIZE_1 = np.array([int(cls.MFCC_SAMPLE_1[i][0].shape[1]//1) for i in range(len(cls.MFCC_SAMPLE_1))])
        # sample 2
        cls.WINDOW_SIZE_2 = np.array([int(cls.MFCC_SAMPLE_2[i][0].shape[1]//1) for i in range(len(cls.MFCC_SAMPLE_2))])
        print('Finish generating window sizes:', (time.time() - start_time))

        # DTW
        # sample 1
        arguments = [(cls.TARGET_FULL_MFCC, cls.MFCC_SAMPLE_1[i][0], cls.WINDOW_SIZE_1[i]) for i in range(len(cls.SAMPLE_WORDS))]
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            results = executor.map(cls.word_spoken_DTW, *zip(*arguments))
        cls.DIST_2D_1 = list(results)
        # sample 2
        arguments = [(cls.TARGET_FULL_MFCC, cls.MFCC_SAMPLE_2[i][0], cls.WINDOW_SIZE_2[i]) for i in range(len(cls.SAMPLE_WORDS))]
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
            results = executor.map(cls.word_spoken_DTW, *zip(*arguments))
        cls.DIST_2D_2 = list(results)
        print('Finish DTW:', (time.time() - start_time))

        # Save graph
        plt.rcParams['figure.figsize'] = (20, 2)
        # sample 1
        cls.clear_folder(os.path.join(cls.PARENT_FOLDER, cls.GRAPH_FOLDER_1))
        for i in range(len(cls.DIST_2D_1)):
            smallest_idx = cls.DIST_2D_1[i].argmin()
            fig, ax = plt.subplots()
            ax.set_title(cls.SAMPLE_WORDS[i])
            ax.set_xlabel('Time (Scaled)')
            ax.set_ylabel('Distance')
            ax.plot(cls.DIST_2D_1[i])
            ax.scatter(smallest_idx, cls.DIST_2D_1[i][smallest_idx], s=50, color='orange')
            fig.savefig(fname=os.path.join(cls.PARENT_FOLDER, cls.GRAPH_FOLDER_1, f'{i+1}_{cls.SAMPLE_WORDS[i]}.jpg'), dpi=200, bbox_inches='tight', pad_inches=0.1)
        # sample 2
        cls.clear_folder(os.path.join(cls.PARENT_FOLDER, cls.GRAPH_FOLDER_2))
        for i in range(len(cls.DIST_2D_2)):
            smallest_idx = cls.DIST_2D_2[i].argmin()
            fig, ax = plt.subplots()
            ax.set_title(cls.SAMPLE_WORDS[i])
            ax.set_xlabel('Time (Scaled)')
            ax.set_ylabel('Distance')
            ax.scatter(smallest_idx, cls.DIST_2D_2[i][smallest_idx], s=50, color='orange')
            ax.plot(cls.DIST_2D_2[i])
            fig.savefig(fname=os.path.join(cls.PARENT_FOLDER, cls.GRAPH_FOLDER_2, f'{i+1}_{cls.SAMPLE_WORDS[i]}.jpg'), dpi=200, bbox_inches='tight', pad_inches=0.1)
        print('Finish producing graphs:', (time.time() - start_time))

        # time ranges
        # sample 1
        cls.TIME_RANGE_1 = [cls.get_timeRange(cls.DIST_2D_1[i], cls.WINDOW_SIZE_1[i]) for i in range(len(cls.SAMPLE_WORDS))]
        # sample 2
        cls.TIME_RANGE_2 = [cls.get_timeRange(cls.DIST_2D_2[i], cls.WINDOW_SIZE_2[i]) for i in range(len(cls.SAMPLE_WORDS))]
        print('Finish calculating time ranges:', (time.time() - start_time))

        # postprocess
        # save to file
        cls.clear_folder(os.path.join(cls.PARENT_FOLDER, cls.DETECTED_FOLDER_1))
        cls.clear_folder(os.path.join(cls.PARENT_FOLDER, cls.DETECTED_FOLDER_2))
        for i, word in enumerate(cls.SAMPLE_WORDS):
            # sample 1
            detected_path_1 = os.path.join(cls.PARENT_FOLDER, cls.DETECTED_FOLDER_1, f'{i+1}_{word}.wav')
            data_1 = cls.TARGET_FULL_AUDIO[cls.TIME_RANGE_1[i][0]:cls.TIME_RANGE_1[i][1]]
            rate_1 = cls.AUDIO_SAMPLE_1[i][1]
            cls.save_mp3(data_1, rate_1, detected_path_1)
            # sample 2
            detected_path_2 = os.path.join(cls.PARENT_FOLDER, cls.DETECTED_FOLDER_2, f'{i+1}_{word}.wav')
            data_2 = cls.TARGET_FULL_AUDIO[cls.TIME_RANGE_2[i][0]:cls.TIME_RANGE_2[i][1]]
            rate_2 = cls.AUDIO_SAMPLE_2[i][1]
            cls.save_mp3(data_2, rate_2, detected_path_2)
        print('Finish output audio files:', (time.time() - start_time))

        # save to json
        raw_data = {}
        # target
        full_target_audio_data = {
            "audio_title": cls.TARGET_AUDIO_NAME,
            "source_link": cls.TARGET_URL,
            "target_audio_path": os.path.join(cls.PARENT_FOLDER, cls.FULL_TARGET_FOLDER, cls.TARGET_AUDIO_NAME).replace("\\", "/"),
            "transcript": cls.FULL_SENTENCE
        }

        raw_data["full_target_audio"] = full_target_audio_data

        # sample 1
        sample_audio_1_data = []
        # sample 2
        sample_audio_2_data = []

        for i, word in enumerate(cls.SAMPLE_WORDS):
            # sample 1
            img_path = os.path.join(cls.PARENT_FOLDER, cls.GRAPH_FOLDER_1, f'{i+1}_{word}.jpg').replace("\\", "/")
            actual_audio_path = os.path.join(cls.PARENT_FOLDER, cls.SAMPLE_FOLDER_1, f'{i+1}_{word}.mp3').replace("\\", "/")
            detected_audio_path = os.path.join(cls.PARENT_FOLDER, cls.DETECTED_FOLDER_1, f'{i+1}_{word}.wav').replace("\\", "/")

            data = {
                "actual_word": word,
                "graph_img_path": img_path,
                "actual_audio_path": actual_audio_path,
                "detected_audio_path": detected_audio_path
            }
            sample_audio_1_data.append(data)

            # sample 2
            img_path = os.path.join(cls.PARENT_FOLDER, cls.GRAPH_FOLDER_2, f'{i+1}_{word}.jpg').replace("\\", "/")
            actual_audio_path = os.path.join(cls.PARENT_FOLDER, cls.SAMPLE_FOLDER_2, f'{i+1}_{word}.mp3').replace("\\", "/")
            detected_audio_path = os.path.join(cls.PARENT_FOLDER, cls.DETECTED_FOLDER_2, f'{i+1}_{word}.wav').replace("\\", "/")

            data = {
                "actual_word": word,
                "graph_img_path": img_path,
                "actual_audio_path": actual_audio_path,
                "detected_audio_path": detected_audio_path
            }
            sample_audio_2_data.append(data)

        raw_data["sample_audio_1"] = sample_audio_1_data
        raw_data["sample_audio_2"] = sample_audio_2_data

        with open('data.json', 'w') as outfile:
            json.dump(raw_data, outfile, indent=4)
        print('Finish output data json:', (time.time() - start_time))

        plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]

    @classmethod
    def load_multi_audio(cls, paths: list) -> list:
        '''Load multiple audio data'''
        new_audio_list = [librosa.load(path) for path in paths]
        # for path in paths:
        #     audio, rate = librosa.load(path)
        #     new_audio_list.append((audio, rate))
        return new_audio_list

    @classmethod
    def convert_MFCC(cls, sample_audio, sample_rate):
        '''Convert to MFCC'''
        x_mfcc = librosa.feature.mfcc(sample_audio, sample_rate)
        x_mfcc = cls.preprocess_mfcc(x_mfcc)
        return (x_mfcc, sample_rate)

    @classmethod
    def word_spoken_DTW(cls, target_mfcc: 'np.ndarray', mfcc_sample: 'np.ndarray', window_size: int):
        '''DTW'''
        new_dist = np.zeros(target_mfcc.shape[1] - window_size)
        for j in range(target_mfcc.shape[1] - window_size):
            part_target_mfcc = target_mfcc[:, j:j+window_size]
            single_dist = dtw(part_target_mfcc.T, mfcc_sample.T, dist=lambda x, y: np.linalg.norm(x - y))[0]
            new_dist[j] = single_dist
        return new_dist

    @classmethod
    def get_timeRange(cls, dists: 'np.ndarray', window_size: int):
        '''Get time range from MFCC'''
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

    @classmethod
    def clear_folder(cls, folder: str):
        '''Clear a folder'''
        if not os.path.exists(folder):
            print('{folder} not exist!')
            return

        for root, dirs, files in os.walk(folder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    @classmethod
    def save_mp3(cls, audio, rate, outFile):
        '''Write out audio as 24bit PCM WAV'''
        sf.write(outFile, audio, rate, subtype='PCM_24')


if __name__ == "__main__":
    tr = AudioAnalysis()
    print(tr.PARENT_FOLDER)
    print(AudioAnalysis.PARENT_FOLDER)
    tr.run_audio_analysis()
