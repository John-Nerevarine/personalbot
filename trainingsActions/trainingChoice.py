from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData


# Show existing trainings
async def callbackShowTrainingsForPlay(callback_query: types.CallbackQuery,
                                       state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        trainings = data['trainings'] = tr.getTrainingsList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if trainings:
        for i, train in enumerate(trainings):
            keyboard['inline_keyboard'].append([{'text': train.name, 'callback_data': i}])

    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите тренировку==</b>' if trainings
                                else '<b>==Нет тренировок==</b>',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.trainingChoice.set()


# Show details about training
async def callbackChoiceTrainingsForPlay(callback_query: types.CallbackQuery,
                                         state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        train = data['train'] = data['trainings'][int(callback_query.data)]
        exercisesInTrain = data['exercisesInTrain'] = tr.getActualTrainingExerciseList(data['train'].id)

    if not exercisesInTrain:
        await bot.edit_message_text('<b>==В тренировке нет упражнений==</b>',
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=kb.backKeyboard)
        return

    exercisesText = ''
    for exe in exercisesInTrain:
        exercisesText += (f'\n‣ <b>{exe.name}</b> на ' + ('повторы' if exe.type == 'reps' else 'время') +
                          f' {exe.sets} с отдыхом между подходами {exe.rest} секунд, вес: {exe.weight}')

    await bot.edit_message_text('<b>==Запустить тренировку?==</b>\n' +
                                f'<b>Тренировка</b> "{train.name}", отдых между упражнениями {train.rest} секунд.\n' +
                                exercisesText,
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.confirmKeyboard)

    async with state.proxy() as data:
        data['trainingText'] = (
                    f'<b>Тренировка</b> "{train.name}", отдых между упражнениями {train.rest} секунд.\n' +
                    exercisesText)


# Add training to GoogleSheets and Database
async def callbackConfirmTrainingsForPlay(callback_query: types.CallbackQuery,
                                          state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        train = data['train']
        exercisesInTrain = data['exercisesInTrain']
        trainingText = data['trainingText']
        data['backTexts'] = data['backTexts'][:-1]
        data['backKeyboards'] = data['backKeyboards'][:-1]
        data['backStates'] = data['backStates'][:-1]

    await bot.edit_message_text('<b>==Запись в базу данных...==</b>\n',
                                callback_query.from_user.id, callback_query.message.message_id)

    tr.pushDataToSheets(callback_query.from_user.id, exercisesInTrain)
    tr.playTraining(train.id, exercisesInTrain)

    await bot.edit_message_text(f'<b>==Тренировка добавлена в таблицу==</b>\n{trainingText}',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.backKeyboard)


def registerHandlers(dp: Dispatcher):
    dp.register_callback_query_handler(callbackShowTrainingsForPlay, lambda c: c.data == 'trainChoice',
                                       state=Trainings.main)
    dp.register_callback_query_handler(callbackConfirmTrainingsForPlay, lambda c: c.data == 'confirm',
                                       state=Trainings.trainingChoice)
    dp.register_callback_query_handler(callbackChoiceTrainingsForPlay, lambda c: c.data != 'back',
                                       state=Trainings.trainingChoice)
