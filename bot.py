import telebot


bot = telebot.TeleBot('5396285529:AAGODUcC6QAr34VbeCACbFfoOcgI2T_Lf5Q')


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Hello {message.chat.first_name} {message.chat.last_name}!")


bot.infinity_polling() 