import streamlit as st
from medical_chatbot.answer_search import *
from medical_chatbot.question_classifier import *
from medical_chatbot.question_parser import *


# from medical_chatbot.visualizer import visual

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        default = "How'you doing?"
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return default
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        return final_answers if final_answers else default


try:
    handler = ChatBotGraph()
except:
    pass
support_query_dict = {
    '疾病症状': '感冒有哪些症状',
    '症状查病': '最近老流鼻涕怎么办',
    '疾病病因': '为什么有的人会难产',
    '疾病并发': '艾滋病的并发症有哪些',
    '疾病忌口': '失眠的人不要吃什么',
    '疾病食疗': '感冒了吃什么好',
    '忌口查询': '哪些人最好不要吃蜂蜜',
    '食物治病': '鹅肉用来治疗什么',
    '疾病吃药': '肝病要吃什么药',
    '药品治病': '板蓝根颗粒治疗什么',
    '疾病待检': '脑膜炎怎么才能查出来',
    '检查项目': '全血细胞计数能查出什么',
    '预防措施': '怎样才能预防肾虚',
    '治疗周期': '感冒要多久才能好',
    '治疗方式': '高血压怎么治',
    '治愈概率': '白血病能治好么',
    '易感人群': '什么人容易得高血压',
    '疾病描述': '糖尿病'
}


def chat_process(select_func, title_holder):
    title_holder.markdown('# ' + select_func.split()[-1].upper())

    holder = st.sidebar.empty()
    query1 = holder.text_input('Input something to find out', '如何预防感冒？')
    query2 = ''
    demo = st.sidebar.checkbox('Show demo query')
    if demo:
        keys = st.sidebar.selectbox('Support query type', list(support_query_dict.keys()))
        query2 = support_query_dict[keys]
        query1 = holder.text_input('Input something to find out', query2)

    # 在demo被勾选的情况下，用户直接更改输入框的内容，也可正常对话
    query = query2 if (demo and query2 == query1) else query1
    answer = handler.chat_main(query)
    if isinstance(answer, list):
        if len(answer) > 1:
            for ans in answer:
                result = ans.split('：')
                st.success(result[0])
                for i in result[1:]:
                    st.write(i)
        else:
            st.success('查询结果')
            st.write(answer[0])
    else:
        st.info('试试别的查法呗？')
    # st.plotly_chart(visual())
