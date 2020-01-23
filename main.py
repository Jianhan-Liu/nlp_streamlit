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

    function_list = ['Texts Summarization',
                     'Entity Extraction (Military News)',
                     'Entity Extraction (Military Biography)',
                     'Medical Chatbot']

    func_dict = {function_list[0]: text_summary,
                 function_list[1]: entity_extractor,
                 function_list[2]: None,
                 function_list[3]: None}

    select_func = st.sidebar.selectbox('', ('-', *function_list))

    if select_func == '-':
        st.sidebar.success('Choose a feature to implement')
    else:
        func_dict[select_func](select_func, title_holder)


if __name__ == '__main__':
    main()
