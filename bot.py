#!venv/bin/python

#v1.00.00 by xx.xx.2022 @John_Nerevarine

from aiogram.utils import executor

import mainMenu, trainingsMenu, support
import dataBase as db
from createBot import dp


def on_startup( ):
    db.sqlStart()

mainMenu.registerHandlers(dp)
trainingsMenu.registerHandlers(dp)
support.registerHandlers(dp)

# STARTING
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
