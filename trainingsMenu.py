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
    await bot.edit_message_text('<b>==Настройки физкультуры==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.trainSettingsKeyboard)

# Show Exercises List
async def callbackShowExercisesList(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    exercises = tr.getExerciseList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if not(exercises):
        keyboard['inline_keyboard'].append([{'text': '>> Добавить упражнение', 'callback_data': 'exeAdd'}])
        keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
        keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

        await bot.edit_message_text('<b>==Нет упражнений==</b>',
            callback_query.from_user.id, callback_query.message.message_id,
            reply_markup=keyboard)
        return

    exercisesListText = ''
    for v in exercises:
        exercisesListText += f'{v[0]} на {"повторы" if v[1] == "reps" else "время"} с весом: {v[2]}\n'


    keyboard['inline_keyboard'].append([{'text': 'Изменить упражнение', 'callback_data': 'exeEdit'}])
    keyboard['inline_keyboard'].append([{'text': 'Добавить упражнение', 'callback_data': 'exeAdd'}])
    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
    keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

    await bot.edit_message_text('<b>==Список упражнений==</b>\n\n'+exercisesListText,
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    async with state.proxy() as data:
        data['exercises'] = exercises

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackTrainingsMain, lambda c: c.data == 'trainMenu', state=MainMenu.start)
    dp.register_callback_query_handler(callbackTrainingsSettings, lambda c: c.data == 'trainSettings', state=Trainings.main)
    dp.register_callback_query_handler(callbackShowExercisesList, lambda c: c.data == 'exeShow', state=Trainings.main)
    trainingsActions.editExercise.registerHandlers(dp)
    trainingsActions.addExercise.registerHandlers(dp)