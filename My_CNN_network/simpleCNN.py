import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.python.keras.models import Sequential
import pandas as pd
import re
# Максимальное количество слов
num_words = 15000
# Максимальная длина новости
max_news_len = 100


def make_set(path):
    return pd.read_csv(path,
                       header=None,
                       names=['class', 'title'],
                       encoding='latin-1')


def make_y_class(arr):
    arr_class = []
    positive = 0
    negative = 0
    for i in arr:
        if i == "positive":
            arr_class.append(1)
            positive += 1
        if i == "negative":
            arr_class.append(0)
            negative += 1
    return arr_class


def preprocess_text(text):
    text = text.lower()
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'USER', text)
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    text = re.sub('([A-Za-z]{3}\-\d{2}-\d{2}\s)?\d{2}\:\d{2}[A|P][M]', ' ', text)
    return text.strip()


def call_network(text):
    model = Sequential()
    model.add(Embedding(num_words, 2, input_length=max_news_len))
    model.add(SimpleRNN(8))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model_save_path='C:\\Users\\Illia\\PycharmProjects\\my_diplom\\Test_network\\best_model\\best_mode_77.h5'
    model.load_weights(model_save_path)
    with open('C:\\Users\\Illia\\PycharmProjects\\my_diplom\\Test_network\\best_model\\tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    new_text=[preprocess_text(t) for t in text]
    sequence = tokenizer.texts_to_sequences(new_text)
    data = pad_sequences(sequence, maxlen=max_news_len)
    result = model.predict(data)
    return result


# text = ["Director of the company was fired", "Apple to Start Reopening Stores in Japan This Week", "TikTok's In-App Revenue Skyrockets During Lockdowns", "Coronavirus is propelling Netflix to new heights but is a crash inevitable?"]
#
#
# text2=["May-26-20 01:49AM  	Dow Jones Futures Jump; Five Titans Near Buy Points In Coronavirus Stock Market Rally Investor's Business Daily",
#        "May-25-20 01:02PM  	Gates Foundation Buys Up Amazon, Apple, Twitter Stock; Trims Berkshire Hathaway Stake SmarterAnalyst",
#        "12:45PM  	Dow Jones Stocks To Buy And Watch In May 2020; Apple, Microsoft Approach New Buy Points Investor's Business Daily",
#        "07:58AM  	Apples Key Weaknesses Investopedia"]
# print(call_network(text2))