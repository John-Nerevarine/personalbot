from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
import trainingsActions
from createBot import MainMenu, Trainings
from createBot import bot
from mainMenu import getBackData


# Trainings menu
async def callbackTrainingsMain(callback_query: types.CallbackQuery,
                                state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Физкультура==</b>',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.trainMainKeyboard)
    await Trainings.main.set()


# Trainings Settings Menu
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

    if not exercises:
        keyboard['inline_keyboard'].append([{'text': '>> Добавить упражнение', 'callback_data': 'exeAdd'}])
        keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
        keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

        await bot.edit_message_text('<b>==Нет упражнений==</b>',
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=keyboard)
        return

    exercisesListText = ''
    exercisesList = []
    for exe in exercises:
        if exe.name not in exercisesList:
            exercisesList.append(exe.name)
            exercisesListText += f'> {exe.name}\n'

    keyboard['inline_keyboard'].append([{'text': 'Изменить упражнение', 'callback_data': 'exeEdit'}])
    keyboard['inline_keyboard'].append([{'text': 'Добавить упражнение', 'callback_data': 'exeAdd'}])
    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
    keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

    await bot.edit_message_text('<b>==Список упражнений==</b>\n\n' + exercisesListText,
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    async with state.proxy() as data:
        data['exercises'] = exercises


# Show Trainings List
async def callbackShowTrainingsList(callback_query: types.CallbackQuery,
                                    state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

    trainings = tr.getTrainingsList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if not trainings:
        keyboard['inline_keyboard'].append([{'text': 'Добавить тренировку', 'callback_data': 'trainAdd'}])
        keyboard['inline_keyboard'].append([{'text': 'Дата последней тенировки', 'callback_data': 'lastDate'}])
        keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
        keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

        await bot.edit_message_text('<b>==Нет тренировок==</b>',
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=keyboard)
        return

    trainingsListText = ''
    for train in trainings:
        trainingsListText += f'> Тренировка "{train.name}", приоритет "{train.priority}"\n'

    keyboard['inline_keyboard'].append([{'text': 'Изменить тренировку', 'callback_data': 'trainEdit'}])
    keyboard['inline_keyboard'].append([{'text': 'Добавить тренировку', 'callback_data': 'trainAdd'}])
    keyboard['inline_keyboard'].append([{'text': 'Дата последней тенировки', 'callback_data': 'lastDate'}])
    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
    keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

    await bot.edit_message_text('<b>==Список тренировок==</b>\n\n' + trainingsListText,
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    async with state.proxy() as data:
        data['trainings'] = trainings


def registerHandlers(dp: Dispatcher):
    dp.register_callback_query_handler(callbackTrainingsMain, lambda c: c.data == 'trainMenu', state=MainMenu.start)
    dp.register_callback_query_handler(callbackTrainingsSettings, lambda c: c.data == 'trainSettings',
                                       state=Trainings.main)
    dp.register_callback_query_handler(callbackShowExercisesList, lambda c: c.data == 'exeShow', state=Trainings.main)
    dp.register_callback_query_handler(callbackShowTrainingsList, lambda c: c.data == 'trainsShow',
                                       state=Trainings.main)
    trainingsActions.editExercise.registerHandlers(dp)
    trainingsActions.addExercise.registerHandlers(dp)
    trainingsActions.addTraining.registerHandlers(dp)
    trainingsActions.editTraining.registerHandlers(dp)
    trainingsActions.trainingChoice.registerHandlers(dp)
    trainingsActions.trainingQuick.registerHandlers(dp)
