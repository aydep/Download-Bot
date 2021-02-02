from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils import TestStates
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN
from ftplib import FTP
from datetime import datetime

import keyboards as kb
import pytube
import os

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

button_hi = KeyboardButton('Привет! 👋')

greet_kb = ReplyKeyboardMarkup().add(button_hi)

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

        # streams = yt.streams.filter(progressive = True)
        #
        # await bot.send_message(msg.from_user.id, "Choose resolution")
        # for v in streams:
        #     ress = str(v).find('res=')
        #     await bot.send_message(msg.from_user.id, str(v)[ress+5:ress+9])

        await bot.send_message(msg.from_user.id, "Choose resolution", reply_markup=kb.kb_res)
        await state.set_state(TestStates.all()[1])
        print("state setted : 1")

    except pytube.exceptions.RegexMatchError:
        await bot.send_message(msg.from_user.id, "incorrect link")

@dp.message_handler(state = TestStates.Q2)
async def get_res(msg: types.Message):

    res = msg.text
    print("choosed resolution : " + res)

    if res[len(res)-1] == 'p':
        video = yt.streams.filter(progressive = True, res = res).first()
    else:
        video = yt.streams.filter(progressive = True, res = res+'p').first()

    await bot.send_message(msg.from_user.id, "Please wait...", reply_markup=kb.ReplyKeyboardRemove())

    print("downloading : " + yt.title + '\n' + str(video))
    video.download()
    print("downloaded")

    video_name = yt.title
    video_name = video_name.replace('/','')
    video_name = video_name.replace('\\','')
    video_name = video_name.replace('*','')
    video_name = video_name.replace('.','')
    video_name = video_name.replace('\"','')
    video_name = video_name.replace('\'','')
    video_name = video_name.replace("|",'')
    video_name = video_name.replace(":",'')
    video_name = video_name.replace("#",'')

    ftp = FTP('c97883yq.beget.tech','c97883yq_dwbot','Onm5b-1ju')
    open_video = open(video_name + '.mp4', "rb")
    ftp.storbinary('STOR ' + video_name + '.mp4', open_video)
    open_video.close()

    print("video recived")

    files = ftp.nlst()
    for v in files:
        timestamp = ftp.voidcmd("MDTM " + v)[4:].strip()
        if (int(timestamp[10:12])-datetime.now().minute >= 10):
            ftp.delete(v)

    ftp.quit()

    print("old videos deleted")

    video_name = video_name.replace(' ', '%20')

    await bot.send_message(msg.from_user.id, "http://c97883yq.beget.tech/DownloadBotTmpVideos/" + video_name + ".mp4")
    await bot.send_message(msg.from_user.id, "File will be deleted in 10 minutes!")

    print("link sended")

    await state.set_state(TestStates.all()[0])

if __name__ == '__main__':
    executor.start_polling(dp)
