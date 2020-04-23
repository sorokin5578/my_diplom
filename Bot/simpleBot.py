import telebot
from Bot.Config import TOKEN
from PoolReq.simplePool import make_work
from ParsingFFIN.simpleParsingFFIN import make_all

bot = telebot.TeleBot(TOKEN)
res = []


@bot.message_handler(commands=['start', 'help'])
def help_command(massage):
    bot.send_message(massage.chat.id, "Введите название или тикер акций (до 5  штук), затем нажмите /done"
                                      "\nОзнакомиться с название компаний или их тикерами можно здесь👇")
    bot.send_message(massage.chat.id, "https://ffin.ru/market/directory/data/")


@bot.message_handler(commands=['done'])
def set_of_stock(massage):
    r = ", ".join(res)
    if len(res) <= 5:
        bot.send_message(massage.chat.id,
                         "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать новости о них!"
                         "\nИли /repeat, чтобы повторить ввод.".format(r))
    else:
        bot.send_message(massage.chat.id,
                         "Ваш портфель акций {0}, слишком велик.\nПопробуйте ввести ещё раз (до 5 штук).".format(r))
        res.clear()


@bot.message_handler(commands=['repeat'])
def repeat_command(massage):
    res.clear()
    bot.send_message(massage.chat.id, "Введите название или тикер акций (до 5  штук), затем нажмите /done")


@bot.message_handler(commands=['info'])
def repeat_command(massage):
    bot.send_message(massage.chat.id, "Пожалуйста, подождите немного, я ищу 🔎")
    length = len(res)
    arr = make_all(res)
    cnt = 0
    info_stock = []
    for key in arr[0]:
        info_stock.clear()
        info_stock.append("🏦 Компания: " + arr[0].get(key)[1])
        info_stock.append("Тикер: " + arr[0].get(key)[2])
        info_stock.append("Ссылка: " + arr[0].get(key)[0])
        el = arr[1][cnt]
        for item1 in el[0]:
            if item1 == "Изменение":
                if el[0].get(item1)[0] == "up":
                    info_stock.append(item1 + ": " + el[0].get(item1)[0] + "📈 " + el[0].get(item1)[1])
                else:
                    info_stock.append(item1 + ": " + el[0].get(item1)[0] + "📉 " + el[0].get(item1)[1])
                continue
            info_stock.append(item1 + ": " + el[0].get(item1))
        if el[1]:
            info_stock.append("📰 Новости: ")
            for item2 in el[1]:
                info_stock.append("🗞 "+item2 + " " + el[1].get(item2))
        else:
            info_stock.append("😢 Новостей пока нет ")
        inf = "\n".join(info_stock)
        bot.send_message(massage.chat.id, inf)
        cnt += 1
    # print(res)
    print(len(arr[0]))
    if length != len(arr[0]):
        bot.send_message(massage.chat.id, "😢 Бот не смог найти все компании, "
                                          "которые вы ввели (проверьте название или тикер)")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def listen_msg(massage):
    res.append(massage.text)
    if len(res)<5:
        bot.send_message(massage.chat.id, "Вы вели {0}, введите ещё название или нажмите /done".format(massage.text))
    else:
        r = ", ".join(res)
        bot.send_message(massage.chat.id,
                         "Ваш портфель акций: {0}.\nНажмите /info, чтобы начать получать новости о них!"
                         "\nИли /repeat, чтобы повторить ввод.".format(r))


bot.polling(none_stop=True)
