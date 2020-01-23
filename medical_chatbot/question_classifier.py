import ahocorasick
import os
import pickle
from collections import defaultdict

from smart_open import open


class QuestionClassifier:
    def __init__(self):
        cur_dir = os.path.dirname(__file__)
        # 特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.department_path = os.path.join(cur_dir, 'dict/department.txt')
        self.check_path = os.path.join(cur_dir, 'dict/check.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        self.producer_path = os.path.join(cur_dir, 'dict/producer.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')

        # 加载特征词
        self.disease_wds = [i.strip() for i in open(self.disease_path, 'r', encoding='utf-8') if i.strip()]
        self.department_wds = [i.strip() for i in open(self.department_path, 'r', encoding='utf-8') if i.strip()]
        self.check_wds = [i.strip() for i in open(self.check_path, 'r', encoding='utf-8') if i.strip()]
        self.drug_wds = [i.strip() for i in open(self.drug_path, 'r', encoding='utf-8') if i.strip()]
        self.food_wds = [i.strip() for i in open(self.food_path, 'r', encoding='utf-8') if i.strip()]
        self.producer_wds = [i.strip() for i in open(self.producer_path, 'r', encoding='utf-8') if i.strip()]
        self.symptom_wds = [i.strip() for i in open(self.symptom_path, 'r', encoding='utf-8') if i.strip()]
        self.deny_words = [i.strip() for i in open(self.deny_path, 'r', encoding='utf-8') if i.strip()]
        self.region_words = set(
            self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds)

        # 构造领域actree
        try:
            self.region_tree = pickle.load(open('data/region_tree.pickle', 'rb'))
        except FileNotFoundError:
            self.region_tree = self.build_actree(self.region_words)
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        # 问句疑问词
        self.symptom_qwds = {'症状', '表征', '现象', '症候', '表现'}
        self.cause_qwds = {'原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成'}
        self.accompany_qwds = {'并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现'}
        self.food_qwds = {'饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品'}
        self.drug_qwds = {'药', '药品', '用药', '胶囊', '口服液', '炎片'}
        self.prevent_qwds = {'预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不', '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不', '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不'}
        self.lasttime_qwds = {'周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年'}
        self.cureway_qwds = {'怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治'}
        self.cureprob_qwds = {'多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医'}
        self.easyget_qwds = {'易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上'}
        self.check_qwds = {'检查', '检查项目', '查出', '检查', '测出', '试出'}
        self.belong_qwds = {'属于什么科', '属于', '什么科', '科室'}
        self.cure_qwds = {'治', '治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途', '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要'}

        print('model init finished ......')
        return

    def classify(self, question):
        '''分类主函数'''
        data = defaultdict(list)
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中所涉及到的实体类型
        types = set([label[0] for label in medical_dict.values()])

        question_types = []

        if 'symptom' in types:
            if self.check_words(self.symptom_qwds, question):
                question_types.append('symptom_disease')  # 症状查疾病

        if 'food' in types:
            if self.check_words(self.food_qwds | self.cure_qwds, question):
                deny_status = self.check_words(self.deny_words, question)
                qs_type = 'food_not_disease' if deny_status else 'food_do_disease'
                question_types.append(qs_type)  # 食物查疾病

        if 'drug' in types:
            if self.check_words(self.cure_qwds, question):
                question_types.append('drug_disease')  # 药品治啥病

        if 'check' in types:
            if self.check_words(self.check_qwds | self.cure_qwds, question):
                question_types.append('check_disease')  # 检查项目查疾病

        if 'disease' in types:
            if self.check_words(self.disease_wds, question):
                question_types.append('disease_symptom')  # 疾病查症状
            if self.check_words(self.cause_qwds, question):
                question_types.append('disease_cause')  # 疾病查病因
            if self.check_words(self.accompany_qwds, question):
                question_types.append('disease_accompany')  # 疾病查并发症状
            if self.check_words(self.food_qwds, question):
                deny_status = self.check_words(self.deny_words, question)
                qs_type = 'disease_not_food' if deny_status else 'disease_do_food'
                question_types.append(qs_type)  # 疾病查忌口与推荐食物
            if self.check_words(self.drug_qwds, question):
                question_types.append('disease_drug')  # 疾病查药品
            if self.check_words(self.check_qwds, question):
                question_types.append('disease_check')  # 疾病检查项目
            if self.check_words(self.prevent_qwds, question):
                question_types.append('disease_prevent')  # 疾病查预防
            if self.check_words(self.lasttime_qwds, question):
                question_types.append('disease_lasttime')  # 疾病查持续时间
            if self.check_words(self.cureway_qwds, question):
                question_types.append('disease_cureway')  # 疾病治疗方式
            if self.check_words(self.cureprob_qwds, question):
                question_types.append('disease_cureprob')  # 疾病查病愈概率
            if self.check_words(self.easyget_qwds, question):
                question_types.append('disease_easyget')  # 疾病查易感人群
            if not question_types:
                question_types.append('disease_desc')

        if not question_types and 'symptom' in types:
            question_types.append('symptom_disease')

        data['question_types'] = question_types
        return data

    def build_wdtype_dict(self):
        result = defaultdict(list)
        type_str = ['disease', 'food', 'symptom', 'department', 'check', 'drug', 'producer']
        type_list = [self.disease_wds, self.food_wds, self.symptom_wds, self.department_wds, self.check_wds,
                     self.drug_wds, self.producer_wds]
        for details, label in zip(type_list, type_str):
            for detail in details:
                result[detail].append(label)
        return result

    @staticmethod
    def build_actree(wordlist):
        '''构造actree，加速过滤'''
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def check_medical(self, question):
        '''问句过滤'''
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    @staticmethod
    def check_words(keywords, query):
        return True if any(query.find(i) != -1 for i in keywords) else False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        if not data:
            break
        print(data)
