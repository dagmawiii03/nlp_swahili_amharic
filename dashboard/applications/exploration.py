import streamlit as st
import pandas as pd
import sys
import pickle


def app():

    st.title("African language Speech Recognition - Speech-to-Text ")

    st.header("Visualization")

    st.subheader("distributon of words for Amharic")
    st.image('data/amh_distribution.png')

    st.subheader("distributon of words for Swahili")
    st.image('data/swahili_distribution.png')

    st.subheader("Data Augmentaion")
    st.image('data/data_augmentation.png')
    
    st.subheader("Feature Extraction")
    st.image('data/feat_extraction.png')

    st.subheader("spectogram")
    st.image('data/spectogram.png')

    st.subheader("Mel-Frequency Cepstral Coefficients")
    st.image('data/mfcc.png')

