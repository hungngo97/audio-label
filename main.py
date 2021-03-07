import streamlit as st
import pandas as pd
import base64
import os
import random
from os import listdir
from os.path import isfile, join
import SessionState
import copy

answers = {}
DEFAULT_OPTION = "Choose one option below"


def audio_section(i, file_name):
    # print('file name', file_name)
    audio_file = open(file_name, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)
    options = copy.deepcopy(random_labels)
    options.insert(0, DEFAULT_OPTION)
    label = st.radio("Audio label", options, key=file_name)
    st.write('You selected label: ' + label + ' for the above sound')
    answers[i] = [file_name, label]


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
    # print('Wav files', wav_files)
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


def render_download_link():
    # for loop through answers, if there's an answer that is unchosen, then do not let the user export answer
    is_complete = True
    for i in answers:
        chosen_label = answers[i][1]
        if chosen_label == DEFAULT_OPTION:
            st.markdown('*Question {} is not chosen*'.format(i + 1))
            is_complete = False
            continue
    if (not is_complete):
        st.markdown('**Cannot export to csv because still miss question(s) above**')
        return
    if (is_complete):
        st.markdown(get_table_download_link(pd.DataFrame.from_dict(answers, orient='index',
                                                                   columns=['file_name', 'chosen_label'])),
                    unsafe_allow_html=True)


DATA_SOUNDS = [x[0] for x in os.walk('./data')]
LABELS = []
for datasound in DATA_SOUNDS:
    if len(datasound) <= len('./data'):
        continue
    LABELS.append(datasound[len('./data/'):])
# print('DATA_SOUNDS',DATA_SOUNDS)
# print('LABELS',LABELS)

SOUND_CLASSES = 5
TRIAL_SAMPLES_PER_CLASS = 5
PREDICTION_SAMPLES_PER_CLASS = 15

# Pick a subset from labels list for users to choose
session = SessionState.get(random_labels=[], random_prediction_files=[])
random_labels = session.random_labels
if len(random_labels) <= 0:
    random_labels = random.sample(LABELS, SOUND_CLASSES)
session.random_labels = random_labels
print('Random labels', random_labels)

# Draw sample classes out for users
st.markdown('**First, you need to get familiar with the sample sounds of what you are going to label**')
for label in random_labels:
    st.markdown('**Audio class**: {}'.format(label))
    render_trial_sound(label, TRIAL_SAMPLES_PER_CLASS)

st.markdown(
    '**Second, these are the audio samples that you need to label to compare the performance with the machine learning model**')
# Draw prediction sounds for users to choose from
# Get random list of files
random_prediction_files = session.random_prediction_files
if (len(random_prediction_files) <= 0):
    random_prediction_files = get_random_prediction_files(random_labels, PREDICTION_SAMPLES_PER_CLASS)
    random.shuffle(random_prediction_files)
session.random_prediction_files = random_prediction_files
for i, f in enumerate(random_prediction_files):
    st.markdown('**Audio Sample No.{}, please listen and answer in the multiple choice below: **'.format(i))
    audio_section(i, f)

st.markdown(
    '**After finished labeling, please click the following button to export CSV results and send it to researchers**')

render_download_link()

# TODO: delete?
st.markdown("**Click reset below to reset all of your choices and give a new set of audio files**")
if st.button("Reset"):
    session.random_labels = []
    session.random_prediction_files = []
    answers = {}

# TODO: accuracy calculator?
