
import sys

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as Queue
else:
    import queue as Queue

import os
import threading
import requests
import json
import csv
import pandas as pd
from sklearn.decomposition import NMF
from collections import Counter
from konlpy.tag import Okt
import numpy as np

class QItem(object):
    def __init__(self, priority, function, *args, **kwargs):
        self.priority = priority
        self.function = function
        self.args = args
        self.kwargs = kwargs
        

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority


class ThreadModel(threading.Thread):
    def __init__(self):
        super(ThreadModel, self).__init__()
        print('init ThreadModel')
        self.q = Queue.PriorityQueue()
        self.stop = False

    def onThread(self, function, *args, **kwargs):
        # self.q.put((100, function, args, kwargs))
        self.q.put(QItem(100, function, *args, **kwargs))

    def onPriorThread(self, function, *args, **kwargs):
        self.q.put(QItem(1, function, *args, **kwargs))


    def run(self):
        self.run_init()

        while True:
            if self.stop:
                break
            try :
                qitem = self.q.get()
                args = qitem.args
                kwargs = qitem.kwargs
                function = qitem.function
                function(*args, **kwargs)

            except Queue.Empty:
                self.idle()

            except KeyboardInterrupt:
                print('Keyboard Interrupt')
                self.stop = True

            except Exception as e:
                print('ThreadModel error ' + str(e))

    def run_init(self):
        pass

    def idle(self):
        pass

    def stopRun(self):
        ru.post_log('Stop flask server')
        self.stop = True

    def emptyQueue(self):
        while not self.q.empty():
            try:
                self.q.get(False)
            except Empty:
                continue
            # q.task_done()
        ru.post_log('Stop - empty queue')

    '''TOPIC MODELING PAGE'''

    def connection_check(self, data):
        print("Client Init : ", data['init'])
        print(data['source'])
        to_server = {'data_type': 'connection_check', 'content': data['init']}
        post_data(to_server)
        
    def get_topic_modeling(self, data, k=5):
        print("get_topic_modeling")
        data = data.decode("utf-8")
        feature = []
        answer = []
        with open("temp.csv", 'w') as file:
            file.write(data)
            file.close()
        with open("temp.csv", 'r', encoding="utf-8") as file:
            d = csv.reader(file)
            header = next(d)
            column_number = header.index('맞춤법 교정 후 문장')
            for row in d:
                feature.append(row[column_number])

        tags = set(['Noun', 'Verb', 'Adjective', 'Adverb'])
        twitter = Okt()

        spamWords = set([
            '하다', '되다', '이다', '있다', '돼다', '위해', '라며', '보다', '되어다', '하는', '이런', '그런', '하는', '이상', '모르다', '모름',
            '깉다', '그라샤', '뭠춘다', '죻뇾', '바늴',
        ])

        word_count = Counter()

        for i, each in enumerate(feature):
            if i % 100 == 0:
                print(i)
            words = []
            each = each.strip()
            pos = twitter.pos(each, norm=True, stem=True)

            word_count.update([word for word, tag in pos if tag in tags and len(word) >1 and word not in spamWords])

        wordsList = []
        raw_text = []
        index2voca = set()


        for i, each in enumerate(feature):
            if i % 100 == 0:
                print(i)
            words = []
            pos = twitter.pos(each, norm=True, stem=True)
            words = [word for word, tag in pos if word_count[word] >= 1]

            if len(words) >= 0:
                print(words)
                index2voca.update(words)
                wordsList.append(words)
                raw_text.append(each)

        index2voca = list(index2voca)
        voca2index = {w: i for i, w in enumerate(index2voca)}

        tdm = np.zeros((len(wordsList), len(index2voca)), dtype=np.float32)
        print("tdm.shape : ", tdm.shape)

        for i, words in enumerate(wordsList):
            for word in words:
                tdm[i, voca2index[word]] += 1
        
        K = int(k)
        nmf = NMF(n_components=K, alpha=0.1)
        W = nmf.fit_transform(tdm)
        H = nmf.components_

        topic_list = []
        print("NMF result")

        for k in range(K):
            print(f"{k + 1}th topic")
            temp_list = []
            for index in H[k].argsort()[::-1][:15]:
                temp_list.append(index2voca[index])
                print(index2voca[index], end=" ")
            topic_list.append(temp_list)
            print()

        to_server = {'data_type': 'topic_modeling_result', 'content': {'result': topic_list, 'k': K}}
        post_data(to_server)
        


"""
POST DATA
"""      
def post_data(data)  :
    """
    Send a dictionary to the client
    """
    root = 'http://localhost:5252'
    path = '/to_client/'
    headers = {'content-type': 'application/json'}

    try:
        requests.post(root + path, json.dumps(data), headers=headers)
    except Exception as e:
        print("Warning : couldn't reach the server", root)
        print(e)

if __name__ == "__main__":
    thread_model = ThreadModel()
    thread_model.start()
    thread_model.onThread(thread_model.stopRun)
