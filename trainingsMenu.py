from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
import trainingDataBase as tr
from createBot import MainMenu, Trainings
from createBot import bot
from mainMenu import getBackData
import trainingsActions

# Trainings menu
async def callbackTrainingsMain(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Физкультура==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.trainMainKeyboard)
    await Trainings.main.set()
     
# Settings Menu
async def callbackTrainingsSettings(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Настройки тренировок==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.trainSettingsKeyboard)

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackTrainingsMain, lambda c: c.data == 'trainMenu', state=MainMenu.start)
    dp.register_callback_query_handler(callbackTrainingsSettings, lambda c: c.data == 'trainSettings', state=Trainings.main)
    trainingsActions.removeExercise.registerHandlers(dp)
    trainingsActions.addExercise.registerHandlers(dp)