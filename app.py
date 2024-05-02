import telebot
from config import TOKEN, values
from extensions import ConvertEx, ValuesConvector

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text =('Чтобы начать работу введите команду боту в следующем формате: \n '
           '<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты,'
           'введите /currencies чтобы узнать список доступных валют')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def available_values(message: telebot.types.Message):
    text = 'Доступный валюты:'
    for i in values.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')
        if len(val) != 3:
            raise ConvertEx('Неверное количество параметров.')
        base, quote, amount = val
        data = ValuesConvector.convert(base, quote, amount)
    except ConvertEx as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комнаду \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {data}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)

