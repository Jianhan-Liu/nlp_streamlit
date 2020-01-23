"""
  @Author       : liujianhan
  @Date         : 2020/1/23 下午2:12
  @Project      : streamlit_nlp
  @FileName     : entity_extractor.py
  @Description  : Placeholder
"""
import sys
sys.path.append('/home/ljh/Projects/ee_rule_ie/')

import streamlit as st

from core.extractor_military_dsti_no_subevents import *
from core.extractor_military_dsti import extractor as extractor_more

news_files_path = '/home/ljh/Projects/InformationExtraction/data/DstiInformationNewList'
extra_files_path = '/home/ljh/Projects/ee_rule_ie/data_path/data/'

id2label = json.load(codecs.open(os.path.join(extra_files_path, 'id2weapon_label.json'), 'r', 'utf-8'))
entity_unique_ending = json.load(codecs.open(os.path.join(extra_files_path, 'entity_special_ending.json'), 'r', 'utf-8'))


def entity_extractor(select_func, title_holder):
    title_holder.markdown(f"# {select_func.upper()}")
    file_index = st.sidebar.number_input("Index of file", min_value=1, max_value=5792, step=1)
    temp_file = json.load(codecs.open(os.path.join(news_files_path, f'{file_index}.json')))

    content_index = st.sidebar.number_input("Index of content", min_value=1, max_value=20, step=1)

    more_or_less = st.sidebar.checkbox('Show more entities if no weapon found')
    extractor_dict = {False: extractor, True: extractor_more}
    result = extractor_dict[more_or_less](temp_file[int(content_index)-1], id2label, entity_unique_ending)

    no_weapon_info = st.empty()

    st.info('Content')
    content = st.empty()
    st.info('People')
    people = st.empty()
    st.info('Organization')
    organization = st.empty()
    st.info('Place')
    place = st.empty()
    st.info('Weapon')
    weapon = st.empty()

    if result:
        relation_entity = result[0]['relation_entity']
        content.markdown(result[0]['content'])
        people.markdown('\n'.join([s['name'] for s in relation_entity if s['label'] == ['人物']]))
        organization.markdown('\n'.join([s['name'] for s in relation_entity if s['label'] == ['组织机构']]))
        place.markdown('\n'.join([s['name'] for s in relation_entity if s['label'] == ['地点']]))
        weapon.markdown('\n'.join([s['name'] for s in relation_entity if not set(s['label'][0]) & set('人物组织机构地点')]))
    else:
        no_weapon_info.warning(f'No weapon entity found in {file_index} file {content_index} content')
