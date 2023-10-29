from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery, MediaGroup, InputMediaDocument
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from text import *
from keyboards import * 
from database import *
import re
import asyncio
import datetime

async def cmdStart(message: types.Message):
    print(message.from_user.id)
    await sql_add_scheduled_mailing(message.from_user.id)
    await bot.send_chat_action(chat_id=message.from_user.id, action=types.ChatActions.UPLOAD_VIDEO)
    with open("v2.1.mp4", "rb") as video_file:
        await bot.send_video(message.from_user.id, video_file)
    await message.answer(text=welcomeMessage)
    await message.answer(text="Планируешь посетить «Зимний прокач»?", reply_markup=secondKeyboard)

async def yesAnswer(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Отлично, лови от нас мотивационное видео, которое будет полезно и поднимет вам настроение.")
    await bot.send_chat_action(chat_id=callback_query.from_user.id, action=types.ChatActions.UPLOAD_VIDEO)
    with open("v2.2.mp4", "rb") as video_file:
        await bot.send_video(callback_query.from_user.id, video_file, width=720, height=1200)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Вы можете перейти по ссылке на наш сайт и оставить заявку на участие.", reply_markup=urlKeyboard)

async def noAnswer(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Не получается приехать😔 Тогда ждем тебя на один из мастер-классов.\nА пока смотрите полезное мотивационное видео, которое поднимет вам настроение. ")
    await bot.send_chat_action(chat_id=callback_query.from_user.id, action=types.ChatActions.UPLOAD_VIDEO)
    with open("v2.2.mp4", "rb") as video_file:
        await bot.send_video(callback_query.from_user.id, video_file, width=720, height=1200)



async def mailing():
    while True:
        try:
            current_time = datetime.datetime.now()
            users_data = await sql_read_scheduled_mailing()  
            
            for user_data in users_data:
                user_id, launch_time, flag = user_data
                launch_datetime = datetime.datetime.strptime(launch_time, "%Y-%m-%d %H:%M:%S")
                
                if current_time - launch_datetime >= datetime.timedelta(days=1) and flag == 0: #days=1
                    try:
                        await bot.send_message(chat_id=user_id, text="Добрый день! Хотим вас зарядить атмосферой на предстоящий интенсив «Зимний прокач 2024».")
                        await bot.send_chat_action(chat_id=user_id, action=types.ChatActions.UPLOAD_VIDEO)
                        with open("v2.3.mp4", "rb") as video_file:
                            await bot.send_video(user_id, video_file, width=1200, height=720)
                        #flag==1
                        await sql_update1_scheduled_mailing(user_id)
                        #await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки
                    except:
                        await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки
                
                if current_time - launch_datetime >= datetime.timedelta(days=7) and flag == 1: #days=1
                    try:
                        await bot.send_message(chat_id=user_id, text="Добрый день! Продолжаем заряжать вас атмосферой на интенсив «Зимний прокач 2024».")
                        await bot.send_chat_action(chat_id=user_id, action=types.ChatActions.UPLOAD_VIDEO)
                        with open("v2.4.mp4", "rb") as video_file:
                            await bot.send_video(user_id, video_file, width=720, height=1200)
                        #flag==2
                        await sql_update2_scheduled_mailing(user_id)
                        #await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки
                    except:
                        await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки

                if current_time >= datetime.datetime(2023,12,1) and flag == 2: #days=1
                    try:
                        await bot.send_message(chat_id=user_id, text="Добрый день! Продолжаем заряжать вас атмосферой на интенсив «Зимний прокач 2024».")
                        await bot.send_chat_action(chat_id=user_id, action=types.ChatActions.UPLOAD_VIDEO)
                        with open("v2.5.mp4", "rb") as video_file:
                            await bot.send_video(user_id, video_file, width=1200, height=720)
                        await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки
                    except:
                        await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки
            await asyncio.sleep(3600) #3600 # Подождите 1 час перед следующей проверкой
        except:
            pass

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmdStart, commands=['start'])
    dp.register_callback_query_handler(yesAnswer, lambda c: c.data == "yes")
    dp.register_callback_query_handler(noAnswer, lambda c: c.data == "no")
