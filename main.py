"""
  User: Liujianhan
  Time: 10:42
 """

import streamlit as st

from summarize.summarize import text_summary
from entity_extractor.entity_extractor import entity_extractor

# TODO memory killer, don't import on local
# from ltp.extractor import Extractor

title_holder = st.empty()


def main():
    st.sidebar.header('Choice Feature to Use')

    func_dict = {'Texts Summarization': text_summary,
                 'Entity Extraction (Military News)': entity_extractor,
                 'Entity Extraction (Military Biography)': None,
                 'Medical Chatbot': None}

    select_func = st.sidebar.selectbox('', ('-', *func_dict.keys()))

    if select_func == '-':
        st.sidebar.success('Choose a feature to implement')
    else:
        func_dict[select_func](select_func, title_holder)


if __name__ == '__main__':
    main()
