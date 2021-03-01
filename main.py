import streamlit as st
import pandas as pd
import base64

LABELS = ('Knocking', 'Speech', "Dog Bark")
files = ['audio1.wav', 'audio2.wav']
answers = {}

def audio_section(file_name):
    audio_file = open('data/' + file_name, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)
    label = st.radio("Audio label", LABELS, key=file_name)
    st.write('Selected ' + label)
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

for f in files:
    audio_section(f)

st.markdown(get_table_download_link(pd.DataFrame.from_dict(answers, orient='index',
                       columns=['chosen_label'])), unsafe_allow_html=True)
