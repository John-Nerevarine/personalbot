from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData
import json

async def callbackShowTrainingsForPlay(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        trainings = data['trainings'] = tr.getTrainingsList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if trainings:
	    for i, v in enumerate(trainings):
	        keyboard['inline_keyboard'].append([{'text': v[0], 'callback_data': i}])

    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите тренировку==</b>' if trainings
    	else '<b>==Нет тренировок==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.trainingChoice.set()

async def callbackChoiceTrainingsForPlay(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exercisesInTrain = data['exercisesInTrain'] = tr.getActualTrainingExerciseList(data['trainings'][int(callback_query.data)][3])
        training = data['trainings'][int(callback_query.data)]

    if not(exercisesInTrain):
    	await bot.edit_message_text('<b>==В тренировке нет упражнений==</b>',
	        callback_query.from_user.id, callback_query.message.message_id,
	        reply_markup=kb.backKeyboard)
    	return

    exercisesText = ''
    for v in exercisesInTrain:
    	exercisesText += (f'\n‣ <b>{v[1]}</b> на ' + ('повторы' if v[2] == 'reps' else 'время') +
    	f' {v[4]} с отдыхом между подходами {v[5]} секунд, вес: {v[3]}')

    await bot.edit_message_text('<b>==Запустить тренировку?==</b>\n' + 
    	f'<b>Тренировка</b> "{training[0]}", отдых между упражнениями {training[2]} секунд.\n' +
    	exercisesText,
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.confirmKeyboard)

async def callbackConfirmTrainingsForPlay(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Всё пока==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.backKeyboard)

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackShowTrainingsForPlay, lambda c: c.data == 'trainChoice', state=Trainings.main)
    dp.register_callback_query_handler(callbackConfirmTrainingsForPlay, lambda c: c.data == 'confirm', state=Trainings.trainingChoice)
    dp.register_callback_query_handler(callbackChoiceTrainingsForPlay, lambda c: c.data != 'back', state=Trainings.trainingChoice)