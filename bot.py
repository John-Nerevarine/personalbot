#!venv/bin/python

from aiogram.utils import executor

import dataBase as db
import mainMenu
import support
import trainingsMenu
from createBot import dp


def on_startup():
    db.sqlStart()


mainMenu.registerHandlers(dp)
trainingsMenu.registerHandlers(dp)
support.registerHandlers(dp)

# STARTING
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
