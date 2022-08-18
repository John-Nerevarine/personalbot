from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import time
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData

async def callbackShowQuickTraining(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    lastTrainingDate = tr.getLastTrainingDate(callback_query.from_user.id)
    currentDate = time.time()

    if currentDate - lastTrainingDate > 604800:
        exercisesInTrain = tr.getOldestTraining(callback_query.from_user.id, priority = 'Высокий')
    else:
        exercisesInTrain = tr.getOldestTraining(callback_query.from_user.id)

    if not(exercisesInTrain):
        await bot.edit_message_text('<b>==Нет тренировок==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.backKeyboard)
        return

    exercisesText = ''
    for v in exercisesInTrain:
        exercisesText += (f'\n‣ <b>{v[1]}</b> на ' + ('повторы' if v[2] == 'reps' else 'время') +
        f' {v[4]} с отдыхом между подходами {v[5]} секунд, вес: {v[3]}')

    trainingText = (
        f'<b>Тренировка</b> "{exercisesInTrain[0][7]}", отдых между упражнениями {exercisesInTrain[0][8]} секунд.\n'
         + exercisesText)

    await bot.edit_message_text('<b>==Быстрая тренировка==</b>\n\n' +
        trainingText + '\nВыбрать эту тренировку?',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.confirmKeyboard)

    async with state.proxy() as data:
         data['exercisesInTrain'] = exercisesInTrain
         data['trainingText'] = trainingText
    await Trainings.qiuckTraining.set()

async def callbackConfirmQuickTraining(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        exercisesInTrain = data['exercisesInTrain']
        trainingText = data['trainingText']
        data['backTexts'] = data['backTexts'][:-1]
        data['backKeyboards'] = data['backKeyboards'][:-1]
        data['backStates'] = data['backStates'][:-1]

    train_id = exercisesInTrain[0][6]

    await bot.edit_message_text('<b>==Запись в базу данных...==</b>\n',
        callback_query.from_user.id, callback_query.message.message_id)

    tr.pushDataToSheets(callback_query.from_user.id, exercisesInTrain)
    tr.playTraining(train_id, exercisesInTrain, callback_query.from_user.id)

    await bot.edit_message_text(f'<b>==Тренировка добавлена в таблицу==</b>\n{trainingText}',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.backKeyboard)

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackShowQuickTraining, lambda c: c.data == 'qStart', state=Trainings.main)
    dp.register_callback_query_handler(callbackConfirmQuickTraining, lambda c: c.data == 'confirm', state=Trainings.qiuckTraining)