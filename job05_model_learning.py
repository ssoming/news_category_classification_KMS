import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

from tensorflow.keras.callbacks import EarlyStopping


# x_train = np.load('data/x_train.npy', allow_pickle=True)
# y_train = np.load('data/y_train.npy', allow_pickle=True)
# x_test = np.load('data/x_test.npy', allow_pickle=True)
# y_test = np.load('data/y_test.npy', allow_pickle=True)
x_train = np.load('data/x_train_wordsize12480.npy', allow_pickle=True)
y_train = np.load('data/y_train_wordsize12480.npy', allow_pickle=True)
x_test = np.load('data/x_test_wordsize12480.npy', allow_pickle=True)
y_test = np.load('data/y_test_wordsize12480.npy', allow_pickle=True)
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

# # SOFT CODING
# # tokenizer pkl 로드 (파일명에 max값 포함되어 있음)
# pkl_files = glob.glob('data/tokenizer_max*.pkl')
# with open(pkl_files[0], 'rb') as f:
#     tokenizer = pickle.load(f)
#
# wordsize = len(tokenizer.word_index) + 1
# maxlen = x_train.shape[1]
# print(f'wordsize: {wordsize}, maxlen: {maxlen}')


model = Sequential()
model.add(Embedding(12480,128, mask_zero=True))     # 300 -> 128 / mask_zero=True
model.build(input_shape=(None,26))
# model.add(Conv1D(32,5,padding = 'same', activation = 'relu'))
# model.add(MaxPooling1D(2))
model.add(Bidirectional(LSTM(64,activation='tanh', return_sequences=True)))
model.add(Dropout(0.3))
model.add(Bidirectional(LSTM(128,activation='tanh', return_sequences=True)))
model.add(Dropout(0.3))
model.add(Bidirectional(LSTM(64,activation='tanh')))
model.add(Dropout(0.3))     # 0.2 -> 0.3
# model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dense(6,activation='softmax'))
model.summary()

early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, mode='max', restore_best_weights=True)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# batch 128 -> 64 / epochs 10 -> 30 / early stopping
fit_hist= model.fit(x_train,y_train,batch_size=64,epochs=30,
                    validation_data=(x_test,y_test), callbacks=[early_stopping], verbose=1)
# fit_hist= model.fit(x_train,y_train,batch_size=128,epochs=10,validation_data=(x_test,y_test),  verbose=1)


score = model.evaluate(x_test,y_test, verbose=0)
print('Final test loss:', score[0])
print('Final test accuracy:', score[1])
model.save('./models/news_section_classifier{}.h5'.format(score[1]))
plt.plot(fit_hist.history['val_accuracy'],label = 'val accuracy')
plt.plot(fit_hist.history['accuracy'],label = 'train accuracy')
plt.legend(loc='lower right')
plt.show()


