from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData

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
        data['train_id'] = data['trainings'][int(callback_query.data)][3]
        exercisesInTrain = data['exercisesInTrain'] = tr.getActualTrainingExerciseList(data['train_id'])
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
    async with state.proxy() as data:
        train_id = data['train_id']
        exercisesInTrain = data['exercisesInTrain']
        data['backTexts'] = data['backTexts'][:-1]
        data['backKeyboards'] = data['backKeyboards'][:-1]
        data['backStates'] = data['backStates'][:-1]

    exercises_list = []
    for v in exercisesInTrain:
        exercises_list.append([v[0], v[2], v[4]])

    await bot.edit_message_text('<b>==Запись в базу данных...==</b>\n',
        callback_query.from_user.id, callback_query.message.message_id)

    tr.pushDataToSheets(callback_query.from_user.id)
    tr.playTraining(train_id, exercises_list, callback_query.from_user.id)

    await bot.edit_message_text('<b>==Тренировка добавлена в таблицу==</b>\nМожно приступать.',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.backKeyboard)

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackShowTrainingsForPlay, lambda c: c.data == 'trainChoice', state=Trainings.main)
    dp.register_callback_query_handler(callbackConfirmTrainingsForPlay, lambda c: c.data == 'confirm', state=Trainings.trainingChoice)
    dp.register_callback_query_handler(callbackChoiceTrainingsForPlay, lambda c: c.data != 'back', state=Trainings.trainingChoice)