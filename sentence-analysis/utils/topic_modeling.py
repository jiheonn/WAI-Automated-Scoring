from konlpy.tag import Okt
from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF
from sklearn.manifold import TSNE
from scipy.sparse import dok_matrix
from collections import Counter
from random import shuffle
from utils.options import spamWords, tags, Category20
import json
import numpy as np
import pandas as pd


def get_topic_modeling(file, extension, num_topic):
    if extension == 'csv':
        df = pd.read_csv(file.stream)
    elif extension == 'xlsx':
        df = pd.read_excel(file)
    else:
        return None, None

    if len(df.columns) > 1:
        return None, None

    df = df.dropna()
    sentences = df.iloc[:,0].tolist()
    twitter = Okt()
    word_count = Counter()

    for i, each in enumerate(sentences):
        words = []
        each = each.strip()
        pos = twitter.pos(each, norm=True, stem=True)
        word_count.update([word for word, tag in pos if tag in tags and len(word) > 1 and word not in spamWords])

    wordsList = []
    raw_text = []
    index2voca = set()

    for i, each in enumerate(sentences):
        words = []
        pos = twitter.pos(each, norm=True, stem=True)
        words = [word for word, tag in pos if word_count[word] >= 3]

        if len(words) >= 0:
            index2voca.update(words)
            wordsList.append(words)
            raw_text.append(each)

    index2voca = list(index2voca)
    voca2index = {w: i for i, w in enumerate(index2voca)}

    tdm = np.zeros((len(wordsList), len(index2voca)), dtype=np.float32)

    for i, words in enumerate(wordsList):
        for word in words:
            tdm[i, voca2index[word]] += 1

    tdm_normalized = normalize(tdm)
    
    K = num_topic
    nmf = NMF(n_components=K, alpha=0.1, max_iter=300)
    W = nmf.fit_transform(tdm)
    H = nmf.components_

    topic_modeling_result = []

    for k in range(K):
        current_topic = []
        for index in H[k].argsort()[::-1][:15]:
            current_topic.append(index2voca[index])
        topic_modeling_result.append(current_topic)

    factorized_matrix_meta = {
        'index2voca': index2voca, 
        'raw_text': raw_text,
        'W': W,
        'H': H,
    }

    return topic_modeling_result, factorized_matrix_meta


def get_tsne(factorized_matrix_meta, version='keywords'):
    if version == 'sentences':
        tsne_matrix = factorized_matrix_meta['W']
    else : 
        tsne_matrix = np.transpose(factorized_matrix_meta['H'])

    # select random index
    if tsne_matrix.shape[0] > 2000:
        selectNum = 2000
    else :
        selectNum = tsne_matrix.shape[0]
    randIndex = np.random.choice(tsne_matrix.shape[0], selectNum, replace=False)
    randIndex.sort()
    
    tsne = TSNE(n_components=2, init='pca', verbose=1)
    W2d = tsne.fit_transform(tsne_matrix[randIndex, :])
    topicIndex = [v.argmax() for v in tsne_matrix[randIndex, :]]

    data = {
        'x': W2d[:, 0].tolist(),
        'y': W2d[:, 1].tolist(),
        'id': [str(i) for i in randIndex],
        'topic': [str(i) for i in topicIndex],  
        'color': [Category20[tsne_matrix.shape[1]%20][i] for i in topicIndex]
    }

    if version == 'sentences':
        data['document'] = [factorized_matrix_meta['raw_text'][randInd][:100] for randInd in randIndex]  
    else :
        data['document'] = [factorized_matrix_meta['index2voca'][i] for i, w in enumerate(randIndex)]

    return data
