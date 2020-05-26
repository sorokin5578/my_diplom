from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, MaxPooling1D, Conv1D, GlobalMaxPooling1D, Dropout, LSTM, GRU
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Максимальное количество слов
num_words = 10000
# Максимальная длина новости
max_news_len = 40
# Количество классов новостей
nb_classes = 3

def make_set(path):
    return pd.read_csv(path,
                    header=None,
                    names=['class', 'title'],
                    encoding='latin-1')

def make_y_class(arr):
    arr_class = []
    for i in arr:
        if i == "neutral":
            arr_class.append(1)
        if i == "positive":
            arr_class.append(2)
        if i == "negative":
            arr_class.append(0)
    return arr_class


train = make_set('train.csv')
news = train['title']
y_train = utils.to_categorical(make_y_class(train['class']), nb_classes)
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(news)
sequences = tokenizer.texts_to_sequences(news)
x_train = pad_sequences(sequences, maxlen=max_news_len)
model_gru = Sequential()
model_gru.add(Embedding(num_words, 32, input_length=max_news_len))
model_gru.add(GRU(16))
model_gru.add(Dense(nb_classes, activation='softmax'))
model_gru.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model_gru.summary()
model_gru_save_path = 'best_model_gru.h5'
checkpoint_callback_gru = ModelCheckpoint(model_gru_save_path,
                                      monitor='val_accuracy',
                                      save_best_only=True,
                                      verbose=1)
history_gru = model_gru.fit(x_train,
                              y_train,
                              epochs=5,
                              batch_size=128,
                              validation_split=0.1,
                              callbacks=[checkpoint_callback_gru])
plt.plot(history_gru.history['accuracy'],
         label='Доля верных ответов на обучающем наборе')
plt.plot(history_gru.history['val_accuracy'],
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

test = make_set('test.csv')
test_sequences = tokenizer.texts_to_sequences(test['title'])
x_test = pad_sequences(test_sequences, maxlen=max_news_len)
y_test = utils.to_categorical(make_y_class(test['class']), nb_classes)
model_gru.load_weights(model_gru_save_path)
model_gru.evaluate(x_test, y_test, verbose=1)


