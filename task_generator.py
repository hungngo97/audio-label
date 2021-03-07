import os
import random
from os import listdir
from os.path import isfile, join
from shutil import copy

used_files = set()
DATA_SOUNDS = [x[0] for x in os.walk('./data')]
LABELS = []
SOUND_CLASSES = 5
TRIAL_SAMPLES_PER_CLASS = 5
PREDICTION_SAMPLES_PER_CLASS = 15
TRIAL_PATH = 'trial'
PREDICTION_PATH = 'prediction'


def generate_samples(labels, trials_per_class):
    """
    Use to generate samples and make sure that they are not the same as previous call of this function.
    @param labels: list of randomly generated labels
    @param trials_per_class: number of trial per class
    @return: a dictionary, where key is the file path, value is the label of that file
    """
    result = {}
    is_all_new_sample = False
    random_wav_files = []
    global used_files
    for label in labels:
        # read the files from the label directory
        label_dir = './data/' + label
        # need to append label dir before its
        wav_files = [label_dir + '/' + f for f in listdir(label_dir) if isfile(join(label_dir, f))]
        while not is_all_new_sample:
            is_all_new_sample = True
            random_wav_files = random.sample(wav_files, trials_per_class)
            for random_wav_file in random_wav_files:
                if random_wav_file in used_files:
                    is_all_new_sample = False
                    break
            if is_all_new_sample:
                break
        is_all_new_sample = False
        for random_wav_file in random_wav_files:
            # result.append(random_wav_file)
            result[random_wav_file] = label
            used_files.add(random_wav_file)
    return result


def generate_labels(labels, sound_classes):
    """
    This function is used to generate and check whether there are enough files left for that labels, in this case 20 files.
    @param labels: list of randomly generated labels
    @param sound_classes: number of sound classes needed
    @return: a list of random labels
    """
    is_enough_file = False
    random_labels = []
    # make sure to generate the label that has more than 15 files left.
    while not is_enough_file:
        is_enough_file = True
        random_labels = random.sample(labels, sound_classes)
        for label in random_labels:
            # read the files from the label directory
            label_dir = './data/' + label
            # need to append label dir before its
            wav_files = [label_dir + '/' + f for f in listdir(label_dir) if isfile(join(label_dir, f))]
            if len(wav_files) < 20:
                is_enough_file = False
                break
    return random_labels


def generate_task(file_list, path, sub_path):
    for file_name, label in file_list.items():
        new_path = os.path.join(path, sub_path, label)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        copy(file_name, new_path)
        os.remove(file_name)

for data_sound in DATA_SOUNDS:
    if len(data_sound) <= len('./data'):
        continue
    LABELS.append(data_sound[len('./data/'):])

# print('DATA_SOUNDS', DATA_SOUNDS)
# print('LABELS', LABELS)

i = 0
while 5400 - len(used_files) > 100:
    random_labels = generate_labels(LABELS, SOUND_CLASSES)

    path = os.path.join('./tasks', 'user' + str(i + 1))
    if not os.path.exists(path):
        os.makedirs(path)
        os.makedirs(os.path.join(path, TRIAL_PATH))
        os.makedirs(os.path.join(path, PREDICTION_PATH))

    prediction_file_list = generate_samples(random_labels, PREDICTION_SAMPLES_PER_CLASS)
    generate_task(prediction_file_list, path, PREDICTION_PATH)

    trial_file_list = generate_samples(random_labels, TRIAL_SAMPLES_PER_CLASS)
    generate_task(trial_file_list, path, TRIAL_PATH)

    print(f'Generated task {i + 1} with labels {random_labels}')
    i += 1
