import streamlit as st


def view_predictions(page=None,results=None):
    if st.session_state.page_select == page:
        st.subheader('Predictions Chart')
        