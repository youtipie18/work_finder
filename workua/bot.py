import threading
import time
import telebot
import os
import multiprocessing

from scrapper import run_spider
from db import Session, Base, engine
from models import User, Job

Base.metadata.create_all(bind=engine)

API_KEY = os.environ["API_KEY"]
bot = telebot.TeleBot(API_KEY)

session = Session()


@bot.message_handler(commands=["start"])
def start(message):
    msg = f"Вітаю {message.from_user.first_name}!\n" \
          f"Це бот для детального пошуку роботи на WorkUA.\n" \
          f"Натисніть /start_notification щоб почати шукати роботу.\n" \
          "Натисніть /stop_notification щоб зупинити пошук."
    bot.send_message(message.chat.id, f"{msg}")


@bot.message_handler(commands=["start_notification"])
def start_notification(message):
    bot.send_message(message.chat.id, "Введіть ключове слово для пошуку роботи:")
    bot.register_next_step_handler(message, add_user_to_db)


def add_user_to_db(message):
    try:
        user = session.query(User).filter_by(user_id=message.chat.id).first()
        if user:
            user.job_title = message.text
        else:
            user = User(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name}", message.text)
        session.add(user)
        session.commit()
        bot.send_message(message.chat.id, "Пошук розпочато!")
    except Exception as error:
        print(error)
        bot.send_message(message.chat.id, "Під час обробки запиту сталась помилка, спробуйте пізніше.")


@bot.message_handler(commands=["stop_notification"])
def stop_notification(message):
    try:
        user = session.query(User).filter_by(user_id=message.chat.id).first()
        if not user:
            bot.send_message(message.chat.id, "Ви не ведете пошук роботи!")
        else:
            session.delete(user)
            session.commit()
            bot.send_message(message.chat.id, "Пошук роботи зупинено!")
    except Exception as error:
        print(error)
        bot.send_message(message.chat.id, "Під час обробки запиту сталась помилка, спробуйте пізніше.")


def send_hourly_message():
    while True:
        time.sleep(5)
        for user in session.query(User).all():
            old_jobs = session.query(Job).all()

            p = multiprocessing.Process(target=run_spider, args=(user.job_title,))
            p.start()
            p.join()

            jobs = session.query(Job).all()

            for job in jobs:
                if job not in old_jobs:
                    desc = " ".join(job.description.replace('\n', ' ').split(' ')[:50])
                    bot.send_message(user.user_id, f"{job.title}\n"
                                                   f"{job.requirements}\n"
                                                   f"{desc}\n"
                                                   f"{job.url}")


message_thread = threading.Thread(target=send_hourly_message)
message_thread.daemon = True
message_thread.start()

if __name__ == '__main__':
    print("Start working!")
    try:
        bot.polling(none_stop=True)
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
