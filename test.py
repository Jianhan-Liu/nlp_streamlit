"""
  @Author       : liujianhan
  @Date         : 2020/1/23 下午4:26
  @Project      : streamlit_nlp
  @FileName     : test.py
  @Description  : Placeholder
"""

from entity_extractor.entity_extractor import *

if __name__ == '__main__':
    import sys
    print(sys.path)
    print(extractor(temp_file[1], id2label, entity_unique_ending))