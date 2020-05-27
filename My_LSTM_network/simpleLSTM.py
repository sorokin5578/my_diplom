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
nb_classes = 2

def make_set(path):
    return pd.read_csv(path,
                    header=None,
                    names=['class', 'title'],
                    encoding='latin-1')

def make_y_class(arr):
    arr_class = []
    for i in arr:
        if i == "positive":
            arr_class.append(1)
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
model = Sequential()
model.add(Embedding(num_words, 8, input_length=max_news_len))
model.add(LSTM(32, recurrent_dropout = 0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model_lstm_save_path = 'best_model_lstm.h5'
checkpoint_callback_lstm = ModelCheckpoint(model_lstm_save_path,
                                      monitor='val_accuracy',
                                      save_best_only=True,
                                      verbose=1)
history = model.fit(np.asarray(x_train).astype('float32').reshape((-1,1)),
                    np.asarray(y_train).astype('float32').reshape((-1,1)),
                    epochs=15,
                    batch_size=128,
                    validation_split=0.1,
                    callbacks=[checkpoint_callback_lstm])
plt.plot(history.history['accuracy'],
         label='Доля верных ответов на обучающем наборе')
plt.plot(history.history['val_accuracy'],
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

test_sequences = tokenizer.texts_to_sequences(x_test)
x_test = pad_sequences(test_sequences, maxlen=max_news_len)
model.load_weights(model_lstm_save_path)
model.evaluate(x_test, y_test, verbose=1)

text = "Director of the company was fired"
sequence = tokenizer.texts_to_sequences([text])
data = pad_sequences(sequence, maxlen=max_news_len)
result = model.predict(data)
print(text)
print(result)
print("-"*10)
text = "Apple to Start Reopening Stores in Japan This Week"
sequence = tokenizer.texts_to_sequences([text])
data = pad_sequences(sequence, maxlen=max_news_len)
result = model.predict(data)
print(text)
print(result)
print("-"*10)
text = "TikTok's In-App Revenue Skyrockets During Lockdowns"
sequence = tokenizer.texts_to_sequences([text])
data = pad_sequences(sequence, maxlen=max_news_len)
result = model.predict(data)
print(text)
print(result)
print("-"*10)
text = "Coronavirus is propelling Netflix to new heightsbut is a crash inevitable?"
sequence = tokenizer.texts_to_sequences([text])
data = pad_sequences(sequence, maxlen=max_news_len)
result = model.predict(data)
print(text)
print(result)
print("-"*10)
