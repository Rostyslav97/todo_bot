from datetime import datetime
import telebot
from models import User, Todo


bot = telebot.TeleBot('5396285529:AAGODUcC6QAr34VbeCACbFfoOcgI2T_Lf5Q')



@bot.message_handler(commands=['start'])
def start_handler(message):
    if not User.select().where(User.chat_id==message.chat.id):
        User.create(chat_id=message.chat.id) 
    bot.send_message(message.chat.id, f"Hello {message.chat.first_name} {message.chat.last_name}!")



@bot.message_handler(commands=['today', 't'])
def get_todo_list(message):
    user = User.get(User.chat_id == message.chat.id)
    todos = Todo.select().where(Todo.user == user, Todo.date == datetime.today())
    message_text = []

    for todo in todos:
        if todo.is_done:
            message_text.append(f"<b><s>{todo.id}. {todo.task}</s></b>\n")
        else:
            message_text.append(f"<b>{todo.id}. {todo.task}</b>\n")

    bot.send_message(message.chat.id, "".join(message_text), parse_mode='HTML')



@bot.message_handler(regexp="\d+ done")
def make_done(message):
    todo_id = message.text.split(' ')[0]
    todo = Todo.get(Todo.id == todo_id)
    todo.is_done = True
    todo.save()

    bot.send_message(message.chat.id, f"{todo.task} is done now")



@bot.message_handler(content_types=['text'])
def create_todo_handler(message):
    user = User.get(User.chat_id==message.chat.id)
    Todo.create(task=message.text, is_done=False, date=datetime.today(), user=user)
    bot.send_message(message.chat.id, "Your todo was saved")



bot.infinity_polling()
