from collections import Counter
from random import shuffle
from scipy.sparse import dok_matrix
from scipy.stats import rankdata
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
import csv
import json
import numpy as np
import os
import pickle
import pandas as pd
import urllib3

# 체언, 용언, 수식언, 독립언, 관계언, 의존형태, 기호 순.

tag = {
    'NNG' : '일반명사', 'NNP' : '고유명사', 'NNB' : '의존명사', 'NP' : '대명사', 'NR' : '수사',
    
    'VV' : '동사', 'VA' : '형용사', 'VX' : '보조용언', 'VCP' : '긍정지정사', 'VCN' : '부정지정사',
    
    'MM' : '관형사', 'MAG' : '일반부사', 'MAJ' : '접속부사',
    
    'IC' : '감탄사',
    
    'JKS' : '주격조사', 'JKC' : '보격조사', 'JKG' : '관형격조사', 'JKO' : '목적격조사', 'JKB' : '부사격조사', 'JKV' : '호격조사',
    'JKQ' : '인용격조사', 'JX' : '보격조사', 'JC' : '접속조사',
    
    'EP' : '선어말어미', 'EF' : '종결어미', 'EC' : '연결어미', 'ETN' : '명사형전성어미', 'ETM' : '관형형전성어미', 
    'XPN' : '체언접두사', 'XSN' : '명사파생접미사', 'XSV' : '동사파생접미사', 'XSA' : '형용사파생접미사', 'XR' : '어근',
    
    'SF' : '마침표, 물음표, 느낌표', 'SP' : '쉼표, 가운뎃점, 콜론, 빗금', 'SS' : '따옴표, 괄호표, 줄표', 'SE' : '줄임표',
    'SO' : '붙임표(물결, 숨김, 빠짐)', 'SL' : '외국어', 'SH' : '한자', 'SW' : '기타 기호(논리 수학기호, 기호 등)',
    'NF' : '명사추정범주', 'NV' : '용언추정범주', 'SN' : '숫자', 'NA' : '분석불능범주',
}

phrase_label = {
    'S' : '문장', 'NP' : '명사구', 'VP' : '동사구', 'AP' : '부사구', 'VNP' : '명사+이다(지정사)', 'DP' : '관용사구', 'IP' : '감탄사',
    
    'PRN' : '삽입어구', 'X' : 'pseudo phrase', 'L' : '부호', 'R' : '부호', 'Q' : '인용절',
    
    'SBJ' : '주격', 'OBJ' : '목적격', 'MOD' : '관형격 수식어', 'AJT' : '부사격 수식어', 'CNJ' : '연결 (~와)', 'CMP' : '보격', 
    'INT' : '독립어', 
}

class ScoreModel():
    def __init__(self, file_path):
        """
        file_path (string) : file path of the set of answers to be compared.
        """
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)
        self.np_statistics = self.data.iloc[:,-7:].to_numpy()
        self.means_ = np.mean(self.np_statistics, axis=0)
        self.vars_ = np.var(self.np_statistics, axis=0)
        self.max_ = np.max(self.np_statistics, axis=0)
        self.min_ = np.min(self.np_statistics, axis=0)
        self.ETRI_API_KEY = "07c42bb7-4e80-4dcf-9c15-dc6ca844d1fb" # 외부에 공유되지 않도록 유의


    def get_score(self, custom_text, option='normalized'):
        """
            get score of the input sentence.
            
            ==IN== 
            custom_text (string) : input sentence
            option (string) ['normalized', 'standard'] 
                            'normalized' : calculate score with normalization scaler
                            'standard' : calculate score with standardization scaler

            ==OUT==
            return (float) : the score of the input sentece
        """
        normalized_array = normalize(self.np_statistics, norm='max', axis=0)
        
        openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
        accessKey = self.ETRI_API_KEY
        analysisCode = "srl"
        
        splited_text = custom_text.split(".")
        splited_arr = []
        for j, text in enumerate(splited_text):
            if len(text) < 1:
                continue

            requestJson = {
                "access_key": accessKey,
                "argument": {
                    "text": text,
                    "analysis_code": analysisCode
                }
            }

            http = urllib3.PoolManager()
            response = http.request(
                "POST",
                openApiURL,
                headers={"Content-Type": "application/json; charset=UTF-8"},
                body=json.dumps(requestJson)
            )

            obj = json.loads(response.data)
            splited_arr.append(obj)
            
        num_verb_mod = 0
        num_verb_phrase_follwing_noun_phrase = 0
        num_noun_phrase_follwed_by_verb_phrase = 0
        num_jks = 0
        num_jkb = 0
        num_jkg = 0
        num_jko = 0

        for j, w in enumerate(splited_arr):
            try:
                dependency_obj = w['return_object']['sentence'][0]['dependency'] # 의존구문 분석 결과
                morp_obj = w['return_object']['sentence'][0]['morp']             # 형태소 분석 결과

            except:
                print(j)

            num_verb_phrase_follwing_noun_phrase += self._count_verb_phrase_follwing_noun_phrase(dependency_obj)    # 3. 바로 앞에 명사구가 있는 동사구의 수
            num_noun_phrase_follwed_by_verb_phrase += self._count_noun_phrase_follwed_by_verb_phrase(dependency_obj)# 4. 3번에 해당하는 명사구의 수
            num_jks += self._count_jks(morp_obj)        # 8. 주격조사의 수
            num_jkb += self._count_jkb(morp_obj)        # 10. 부사격조사의 수
            num_jkg += self._count_jkg(morp_obj)        # 11. 관형격조사의 수
            num_jko += self._count_jko(morp_obj)        # 12. 목적격조사의 수

        result = np.array([num_verb_mod, num_verb_phrase_follwing_noun_phrase, num_noun_phrase_follwed_by_verb_phrase, \
                                num_jks, num_jkb, num_jkg, num_jko])
        
        if option == 'standard':
            score = np.mean((result-self.means_)/(np.sqrt(self.vars_)))
        else:
            score = np.mean((result-self.min_)/(self.max_-self.min_))

        return score

    def _count_verb_phrase(self, obj):
        """
        1. 동사구의 수
        
        obj : 의존구문 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['label'] == 'VP':
                cnt+=1
        return cnt

    def _count_verb_mod(self, obj):
        """
        2. 동사구-관형격 수식어(일반 동사구 미포함) 수
        
        obj : 의존구문 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['label'] == 'VP_MOD':
                cnt+=1
        return cnt

    def _count_verb_phrase_follwing_noun_phrase(self, obj):
        """
        3. 바로앞에 명사구(모든 형태의 명사구 포함)가 있는 동사구(모든 형태의 동사구 포함)의 수 
        
        obj : 의존구문 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if 'VP' in w['label']:
                try :
                    if 'NP' in obj[i - 1]['label']:
                        cnt+=1
                except :
                    continue
        return cnt

    def _count_noun_phrase_follwed_by_verb_phrase(self, obj):
        """
        4. 3에 해당하는 동사구 앞에 있는 연속된 모든 명사구의 합
        
        obj : 의존구문 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if 'VP' in w['label']:
                try :
                    j = 1
                    while 'NP' in obj[i - j]['label']:
                        cnt+=1
                        j+=1
                        if i - j < 0:
                            break
                except :
                    continue
        return cnt

    def _count_custom_hypothesis(self, obj):
        """
        5. 가정 : 의존구문 분석에서 다음과 같은 상황에서 카운트.
        (1) : '동사구'가 ~면으로 끝나는 경우.
        (2) : '동사구-관형격 수식어', '명사구-부사격 수식어'가 연속으로 나오고 '때'가 있을 때
        
        obj : 의존구문 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['label'] == 'VP':
                if w['text'][-1] == '면':
                    cnt+=1
            try :
                if w['label'] == 'VP_MOD' and obj[i + 1]['label'] == 'NP_CNJ':
                    if '때' in obj[i + 1]['text'][-1]:
                        cnt+=1
            except :
                continue
        return cnt

    def _count_cause_phrase(self, obj):
        """
        6. 원인 : 의존구문 분석에서 동사구에 '~하여', '~해서' 가 있거나 
        '때문', '이유', '원인', '까닭' 이라는 단어가 있을 때
        
        obj : 의존구문 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if 'VP' in w['label']:
                if '하여' in w['text'] or '해서' in w['text']:
                    cnt+=1
            cause_words = ['때문', '이유', '원인', '까닭']
            
            for j, jw in enumerate(cause_words):
                if jw in w['text']:
                    cnt+=1
        return cnt
            
    def _count_jks(self, obj):
        """
        8. 주격조사의 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'JKS':
                cnt+=1
        return cnt

    def _count_jkc(self, obj):
        """
        9. 보격조사의 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'JKC':
                cnt+=1
        return cnt

    def _count_jkb(self, obj):
        """
        10. 부사격조사의 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'JKB':
                cnt+=1
        return cnt

    def _count_jkg(self, obj):
        """
        11. 관형격조사의 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'JKG':
                cnt+=1
        return cnt

    def _count_jko(self, obj):
        """
        12. 목적격조사의 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'JKO':
                cnt+=1
        return cnt

    def _count_nng(self, obj):
        """
        13. 일반명사 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'NNG':
                cnt+=1
        return cnt

    def _count_vv(self, obj):
        """
        14. 동사 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'VV':
                cnt+=1
        return cnt

    def _count_ec(self, obj):
        """
        15. 연결어미 수
        
        obj : 형태소 분석 결과
        """
        cnt = 0
        for i, w in enumerate(obj):
            if w['type'] == 'EC':
                cnt+=1
        return cnt

    def _count_dot(self, string):
        """
        16. 마침표 수 
        
        obj : 맞춤법 교정 후 문장
        """
        return string.count('.')
