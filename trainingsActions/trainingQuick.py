from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import time
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData


# Show optimal training
async def callbackShowQuickTraining(callback_query: types.CallbackQuery,
                                    state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    lastTrainingDate = tr.getLastTrainingDate(callback_query.from_user.id)
    currentDate = time.time()

    if currentDate - lastTrainingDate > 604800:
        train, exercises = tr.getOldestTraining(callback_query.from_user.id, priority='Высокий')
    else:
        train, exercises = tr.getOldestTraining(callback_query.from_user.id)

    if not exercises:
        await bot.edit_message_text('<b>==Нет тренировок==</b>',
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=kb.backKeyboard)
        return

    exercisesText = ''
    for exe in exercises:
        exercisesText += (f'\n‣ <b>{exe.name}</b> на ' + ('повторы' if exe.type == 'reps' else 'время') +
                          f' {exe.sets} с отдыхом между подходами {exe.rest} секунд, вес: {exe.weight}')

    trainingText = (
            f'<b>Тренировка</b> "{train.name}", отдых между упражнениями {train.rest} секунд.\n'
            + exercisesText)

    await bot.edit_message_text('<b>==Быстрая тренировка==</b>\n\n' +
                                trainingText + '\nВыбрать эту тренировку?',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.confirmKeyboard)

    async with state.proxy() as data:
        data['exercises'] = exercises
        data['train'] = train
        data['trainingText'] = trainingText
    await Trainings.qiuckTraining.set()


# Add training to GoogleSheets and Database
async def callbackConfirmQuickTraining(callback_query: types.CallbackQuery,
                                       state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        exercises = data['exercises']
        train = data['train']
        trainingText = data['trainingText']
        data['backTexts'] = data['backTexts'][:-1]
        data['backKeyboards'] = data['backKeyboards'][:-1]
        data['backStates'] = data['backStates'][:-1]

    await bot.edit_message_text('<b>==Запись в базу данных...==</b>\n',
                                callback_query.from_user.id, callback_query.message.message_id)

    tr.pushDataToSheets(callback_query.from_user.id, exercises)
    tr.playTraining(train.id, exercises, callback_query.from_user.id)

    await bot.edit_message_text(f'<b>==Тренировка добавлена в таблицу==</b>\n{trainingText}',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.backKeyboard)


def registerHandlers(dp: Dispatcher):
    dp.register_callback_query_handler(callbackShowQuickTraining, lambda c: c.data == 'qStart', state=Trainings.main)
    dp.register_callback_query_handler(callbackConfirmQuickTraining, lambda c: c.data == 'confirm',
                                       state=Trainings.qiuckTraining)
