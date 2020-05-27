from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, MaxPooling1D, Conv1D, GlobalMaxPooling1D, Dropout, LSTM, GRU
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
from sklearn.model_selection import train_test_split
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


dataset = make_set('all-data.csv')
news = dataset['title']
label = utils.to_categorical(make_y_class(dataset['class']), nb_classes)
x_train, x_test, y_train, y_test = train_test_split(news, label, test_size=0.1, random_state=42)
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(x_train)
sequences = tokenizer.texts_to_sequences(x_train)
x_train = pad_sequences(sequences, maxlen=max_news_len)
model_lstm = Sequential()
model_lstm.add(Embedding(num_words, 32, input_length=max_news_len))
model_lstm.add(LSTM(16))
model_lstm.add(Dense(nb_classes, activation='softmax'))
model_lstm.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model_lstm.summary()
model_lstm_save_path = 'best_model_lstm.h5'
checkpoint_callback_lstm = ModelCheckpoint(model_lstm_save_path,
                                      monitor='val_accuracy',
                                      save_best_only=True,
                                      verbose=1)
history_lstm = model_lstm.fit(x_train,
                              y_train,
                              epochs=5,
                              batch_size=128,
                              validation_split=0.1,
                              callbacks=[checkpoint_callback_lstm])
plt.plot(history_lstm.history['accuracy'],
         label='Доля верных ответов на обучающем наборе')
plt.plot(history_lstm.history['val_accuracy'],
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

test_sequences = tokenizer.texts_to_sequences(x_test)
x_test = pad_sequences(test_sequences, maxlen=max_news_len)
model_lstm.load_weights(model_lstm_save_path)
model_lstm.evaluate(x_test, y_test, verbose=1)


