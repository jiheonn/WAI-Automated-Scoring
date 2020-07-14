from collections import Counter
from konlpy.tag import Okt

tags = set(['Noun', 'Verb', 'Adjective', 'Adverb'])

spamWords = set([
    '하다', '되다', '이다', '있다', '돼다', '위해', '라며', '보다', '되어다', '하는', '이런', '그런', '하는', '이상', '모르다', '모름'
])

def get_tokenized_words(sentences):
    twitter = Okt()
    word_count = Counter()
    pos = twitter.pos(sentences, norm=True, stem=True)
    tokenized = [word for word, tag in pos if tag in tags and len(word) > 1 and word not in spamWords]
    word_count.update(tokenized)
    # the most frequent word in the counter.
    most_common, _ = word_count.most_common()[0] 
    return tokenized, most_common
