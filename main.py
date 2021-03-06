import streamlit as st
import pandas as pd
import base64
import os
import random
from os import listdir
from os.path import isfile, join

answers = {}

def audio_section(file_name):
    print('file name', file_name)
    audio_file = open(file_name, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)
    label = st.radio("Audio label", LABELS, key=file_name)
    st.write('You selected label: ' + label + ' for the above sound')
    answers[file_name] = [label]


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
    return href

def render_trial_sound(label, trials_per_class):
    # read the files from the label directory
    label_dir = './data/' + label
    wav_files = [f for f in listdir(label_dir) if isfile(join(label_dir, f))]
    print('Wav files', wav_files)
    # render samples sounds
    random_wav_files = random.sample(wav_files, trials_per_class)
    for wav_file in random_wav_files:
        audio_file = open(label_dir + '/' + wav_file, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes)

# Return list of random files from each label
def get_random_prediction_files(labels, trials_per_class):
    result = []
    for label in labels:
        # read the files from the label directory
        label_dir = './data/' + label
        # need to append label dir before it
        wav_files = [label_dir + '/' + f for f in listdir(label_dir) if isfile(join(label_dir, f))]
        random_wav_files = random.sample(wav_files, trials_per_class)
        for random_wav_file in random_wav_files:
            result.append(random_wav_file)
    return result


DATA_SOUNDS = [x[0] for x in os.walk('./data')]
LABELS = []
for datasound in DATA_SOUNDS:
    if len(datasound) <= len('./data'):
        continue
    LABELS.append(datasound[len('./data/'):])
print(DATA_SOUNDS)
print(LABELS)

SOUND_CLASSES = 5
TRIAL_SAMPLES_PER_CLASS = 5
PREDICTION_SAMPLES_PER_CLASS = 15

# Pick a subset from labels list for users to choose
random_labels = random.sample(LABELS, SOUND_CLASSES)
print('Random labels', random_labels)

# Draw sample classes out for users
st.markdown('**First, you need to get familiar with the sample sounds of what you are going to label**')
for label in random_labels:
    st.markdown('**Audio class**: {}'.format(label))
    render_trial_sound(label, TRIAL_SAMPLES_PER_CLASS)


st.markdown('**Second, these are the audio samples that you need to label to compare the performance with the machine learning model**')
# Draw prediction sounds for users to choose from
# Get random list of files
random_prediction_files = get_random_prediction_files(random_labels, PREDICTION_SAMPLES_PER_CLASS)
for i, f in enumerate(random_prediction_files):
    st.markdown('**Audio Sample No.{}, please listen and answer in the multiple choice below: **'.format(i))
    audio_section(f)


st.markdown('**After finished labeling, please click the following button to export CSV results and send it to researchers**')
st.markdown(get_table_download_link(pd.DataFrame.from_dict(answers, orient='index',
                       columns=['chosen_label'])), unsafe_allow_html=True)
