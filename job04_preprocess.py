import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt, Komoran
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import re
import datetime     # 내장 라이브러리


df = pd.read_csv('data/news_titles_20260608.csv')
df.info()
print(df.head(30))
print(df.category.value_counts())


X = df.title
Y = df.category
# print(X[3])
# okt = Okt()
# okt_x = okt.morphs(X[3])
# print(okt_x)
#
# okt_x_stem = okt.morphs(X[3],stem= True) #stem= True형태소를 위해서 (동사 원형으로)
# print(okt_x_stem)
# exit()
#
# komoran = Komoran()
# komoran_x = komoran.morphs(X[0])
# print(komoran_x)

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
with open('data/encoder.pkl', 'wb') as f:
    pickle.dump(encoder,f)

onehot_y = to_categorical(labeled_y)
print(onehot_y[:5])

# cleanned_x = re.sub('[^가-힣]', ' ', X[0])
# print(X[0])
# print(cleanned_x)

X = list(X)
okt = Okt()

for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ' , X[i])
    X[i] =okt.morphs(X[i], stem=True)

    if i % 1000==0:
        print(i)
print(X[:5])
for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word)>1:
            words.append(word)
    X[idx] = ' '.join(words)
print(X[:5])
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
tokened_x = tokenizer.texts_to_sequences(X)
print(tokened_x)

wordsize = len(tokenizer.word_index) + 1
print(wordsize)
max = 0

#문장의 길이르 맞춤
for sentence in tokened_x:
    if max< len(sentence):
        max = len( sentence )
print(max)
with open('data/tokenizer_max{}.pkl'.format(max), 'wb') as f:
    pickle.dump(tokenizer,f)

x_pad = pad_sequences(tokened_x, maxlen=max)
print(x_pad[:5])

x_train, x_test, y_train, y_test = train_test_split(x_pad, onehot_y, test_size=0.1)
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

np.save('./data/x_train_wordsize{}.npy'.format(wordsize), x_train)
np.save('./data/y_train_wordsize{}.npy'.format(wordsize), y_train)
np.save('./data/x_test_wordsize{}.npy'.format(wordsize), x_test)
np.save('./data/y_test_wordsize{}.npy'.format(wordsize), y_test)


# np.save('./data/x_train.npy'.format(wordsize), x_train)
# np.save('./data/y_train.npy'.format(wordsize), y_train)
# np.save('./data/x_test.npy'.format(wordsize), x_test)
# np.save('./data/y_test.npy'.format(wordsize), y_test)
