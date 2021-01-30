from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils import TestStates

from config import TOKEN

import pytube
import os

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(state='*', commands=['start'])
async def start_command(msg: types.Message):
    global state
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(TestStates.all()[0])
    await bot.send_message(msg.from_user.id, "Enter video link")
    print("entered command : start")

@dp.message_handler(state = TestStates.Q1)
async def get_url(msg: types.Message):
    url = msg.text
    try:
        global yt
        yt = pytube.YouTube(url)

        await bot.send_message(msg.from_user.id, yt.title + '\n\n' + yt.author)

        streams = yt.streams.filter(progressive = True)

        await bot.send_message(msg.from_user.id, "Choose resolution")
        for v in streams:
            ress = str(v).find('res=')
            await bot.send_message(msg.from_user.id, str(v)[ress+5:ress+9])

        await state.set_state(TestStates.all()[1])

    except pytube.exceptions.RegexMatchError:
        await bot.send_message(msg.from_user.id, "incorrect link")

@dp.message_handler(state = TestStates.Q2)
async def get_res(msg: types.Message):

    res = msg.text
    print(res)

    if res[len(res)-1] == 'p':
        video = yt.streams.filter(progressive = True, res = res).first()
    else:
        video = yt.streams.filter(progressive = True, res = res+'p').first()

    await bot.send_message(msg.from_user.id, "Please wait...")

    print("Downloading: " + str(video))
    video.download()
    print("Downloaded " + yt.title + ".mp4")

    video_name = yt.title
    video_name = video_name.replace('/','')
    video_name = video_name.replace('*','')
    video_name = video_name.replace('.','')
    print(video_name)

    open_video = open(video_name + '.mp4', "rb")
    await bot.send_document(msg.from_user.id, open_video)
    open_video.close()
    await bot.send_message(msg.from_user.id, "Done!")

    await state.set_state(TestStates.all()[0])

if __name__ == '__main__':
    executor.start_polling(dp)
