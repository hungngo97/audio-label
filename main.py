import streamlit as st
audio_file = open('audio1.wav', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes)


label = st.radio("Audio label", ('Knocking', 'Speech', "Dog Bark"))
st.write('Selected ' + label)