from datetime import datetime
from threading import Thread
import telebot
from models import User, Todo
import schedule
import time


bot = telebot.TeleBot('5396285529:AAGODUcC6QAr34VbeCACbFfoOcgI2T_Lf5Q')



@bot.message_handler(commands=['start'])
def start_handler(message):
    if not User.select().where(User.chat_id==message.chat.id):
        User.create(chat_id=message.chat.id) 
    bot.send_message(message.chat.id, f"Hello {message.chat.first_name} {message.chat.last_name}!")


def create_all_todo_message(chat_id):
    user = User.get(User.chat_id == chat_id)
    todos = Todo.select().where(Todo.user == user, Todo.date == datetime.today())
    message_text = []

    for todo in todos:
        if todo.is_done:
            message_text.append(f"<b><s>{todo.id}. {todo.task}</s></b>\n")
        else:
            message_text.append(f"<b>{todo.id}. {todo.task}</b>\n")
    
    return "".join(message_text)



@bot.message_handler(commands=['today', 't'])
def get_todo_list(message):
    bot.send_message(message.chat.id, create_all_todo_message(message.chat.id), parse_mode='HTML')



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



def check_notify():
    for user in User.select():
        todos = Todo.select().where(Todo.user == user, Todo.date == datetime.today(), Todo.is_done == False)
        if todos:
            bot.send_message(user.chat_id,create_all_todo_message(user.chat_id), parse_mode='HTML')



def run_scheduler():
    schedule.every(1).hours.do(check_notify)
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == "__main__":
    Thread(target=run_scheduler).start()
    bot.infinity_polling()
