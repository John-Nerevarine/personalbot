from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData
import datetime


# Show menu from existing trainings
async def callbackShowTrainingsForEdit(callback_query: types.CallbackQuery,
                                       state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        trainings = data['trainings']

    keyboard = {"inline_keyboard": []}
    for i, train in enumerate(trainings):
        keyboard['inline_keyboard'].append([{'text': train.name, 'callback_data': i}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите тренировку==</b>',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.editTrainingSetName.set()


# Show available editing options and actions for the training
async def callbackEditTraining(callback_query: types.CallbackQuery,
                               state: FSMContext):
    i = int(callback_query.data)
    async with state.proxy() as data:
        data['train'] = train = data['trainings'][i]
        data['i'] = i
        data['exercisesInTrain'] = exercisesInTrain = tr.getExercisesInTrain(train.id)
        data['stage'] = 'choice'
        data['temp'] = 0

    keyboard = {"inline_keyboard": []}
    keyboard['inline_keyboard'].append([{'text': 'Изменить название', 'callback_data': 'editName'}])
    keyboard['inline_keyboard'].append([{'text': 'Изменить приоритет', 'callback_data': 'editPriority'}])
    keyboard['inline_keyboard'].append([{'text': 'Изменить время отдыха', 'callback_data': 'editRest'}])
    keyboard['inline_keyboard'].append([{'text': 'Добавить упражнение', 'callback_data': 'addExe'}])

    exercisesText = ''
    if exercisesInTrain:
        for exe_name in exercisesInTrain:
            exercisesText += exe_name + '\n'
        keyboard['inline_keyboard'].append([{'text': 'Удалить упражнение', 'callback_data': 'removeExe'}])
    else:
        exercisesText = 'В тренировке нет упражнений.'

    keyboard['inline_keyboard'].append([{'text': 'Удалить тренировку', 'callback_data': 'removeTrain'}])
    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n' +
                                f'<b>Название тренировки:</b> <i>{train.name}</i>\n' +
                                f'<b>Приоритет тренировки:</b> <i>{train.priority}</i>\n' +
                                f'<b>Время отдыха между упражнениями:</b> <i>{train.rest}</i>\n' +
                                f'<b>Упражнения:</b>\n<i>{exercisesText}</i>\n',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.editTraining.set()


# Entering new name for the training
async def callbackEditTrainingName(callback_query: types.CallbackQuery,
                                   state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n' +
                                'Введите новое название  (max. 34):',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'name'


# Choosing new priority for the training
async def callbackEditTrainingPriority(callback_query: types.CallbackQuery,
                                       state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n' +
                                'Выберите приоритет.',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.trainPriorityKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'priority'

    await Trainings.editTrainingSetPriority.set()


# Set new priority for the training
async def callbackEditTrainingPrioritySet(callback_query: types.CallbackQuery,
                                          state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.editTraining(data['train'].id, 'priority', callback_query.data)

        data['backTexts'][-2] = data['backTexts'][-2].replace(
            'Тренировка "' + data['train'].name + '", приоритет "' + data['train'].priority + '"',
            'Тренировка "' + data['train'].name + '", приоритет "' + callback_query.data + '"')

        data['train'].priority = callback_query.data

    await showEditedTrainingMessage(callback_query.from_user.id, state)
    await Trainings.editTraining.set()


# Entering new rest time for the training
async def callbackEditTrainingRest(callback_query: types.CallbackQuery,
                                   state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n' +
                                'Введите время отдыха:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'rest'


# Show exercises to add in the training
async def callbackEditTrainingAddExe(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    exercises = tr.getExerciseList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if not exercises:
        await bot.edit_message_text('<b>==Нет упражнений==</b>',
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=kb.backKeyboard)
        return

    names = []
    for exe in exercises:
        if exe.name not in names:
            names.append(exe.name)

    for name in names:
        keyboard['inline_keyboard'].append([{'text': name, 'callback_data': name}])

    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n' +
                                'Ввыберите упражнение, которое хотите добавить:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.editTrainingAddExe.set()


# Adding the exercise in the training
async def callbackEditTrainingAddExeChoice(callback_query: types.CallbackQuery,
                                           state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        if callback_query.data in data['exercisesInTrain']:
            await bot.edit_message_text('<b>==Это упражнение уже есть в тренировке==</b>\n\n',
                                        callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=kb.backKeyboard)
        else:
            tr.addExerciseInTrain(data['train'].id, callback_query.data)
            data['exercisesInTrain'].append(callback_query.data)

            await bot.edit_message_text('<b>==Упражнение добавлено в тренировку.==</b>',
                                        callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=kb.backKeyboard)

            if 'В тренировке нет упражнений.' in data['backTexts'][-2]:
                data['backTexts'][-2] = data['backTexts'][-2].replace(
                    'В тренировке нет упражнений.',
                    f'<i>{callback_query.data}</i>')
            else:
                data['backTexts'][-2] += f'\n<i>{callback_query.data}</i>'


# Show exercises to remove from training
async def callbackEditTrainingRemoveExe(callback_query: types.CallbackQuery,
                                        state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        exercisesInTrain = data['exercisesInTrain']

    keyboard = {"inline_keyboard": []}

    if not exercisesInTrain:
        await bot.edit_message_text('<b>==Нет упражнений==</b>',
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=kb.backKeyboard)
        return

    for name in exercisesInTrain:
        keyboard['inline_keyboard'].append([{'text': name, 'callback_data': name}])

    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n' +
                                'Ввыберите упражнение, которое хотите удалить:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.editTrainingRemoveExe.set()


# Removing the exercise from the training
async def callbackEditTrainingRemoveExeChoice(callback_query: types.CallbackQuery,
                                              state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.removeExerciseFromTrain(data['train'].id, callback_query.data)
        data['exercisesInTrain'].remove(callback_query.data)

        data['backTexts'][-2] = data['backTexts'][-2].replace(
            callback_query.data, '')

        i = 0
        flag = True
        while flag and i < len(data['backKeyboards'][-1]['inline_keyboard']):
            if data['backKeyboards'][-1]['inline_keyboard'][i][0]['text'] == callback_query.data:
                data['backKeyboards'][-1]['inline_keyboard'].pop(i)
                flag = False
            i += 1

    await bot.edit_message_text('<b>==Упражнение удалено из тренировки.==</b>',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.backKeyboard)


# Removing the training
async def callbackEditTrainingRemoveTrain(callback_query: types.CallbackQuery,
                                          state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.removeTraining(data['train'].id)

        data['backTexts'][-1] = data['backTexts'][-1].replace('> Тренировка "' + data['train'].name +
                                                              '", приоритет "' + data['train'].priority + '"',
                                                              '')
        data['trainings'].pop(data['i'])

    await bot.edit_message_text('<b>==Тренировка удалена==</b>\n\n',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.backKeyboard)


# Show message with edited training
async def showEditedTrainingMessage(user_id, state: FSMContext):
    async with state.proxy() as data:
        keyboard = {"inline_keyboard": []}
        keyboard['inline_keyboard'].append([{'text': 'Изменить название', 'callback_data': 'editName'}])
        keyboard['inline_keyboard'].append([{'text': 'Изменить приоритет', 'callback_data': 'editPriority'}])
        keyboard['inline_keyboard'].append([{'text': 'Изменить время отдыха', 'callback_data': 'editRest'}])
        keyboard['inline_keyboard'].append([{'text': 'Добавить упражнение', 'callback_data': 'addExe'}])

        exercisesText = ''
        if data['exercisesInTrain']:
            for name in data['exercisesInTrain']:
                exercisesText += name + '\n'
            keyboard['inline_keyboard'].append([{'text': 'Удалить упражнение', 'callback_data': 'removeExe'}])
        else:
            exercisesText = 'В тренировке нет упражнений.'

        keyboard['inline_keyboard'].append([{'text': 'Удалить тренировку', 'callback_data': 'removeTrain'}])
        keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])

        await bot.edit_message_text('<b>==Тренировка изменена!==</b>\n\n' +
                                    f'<b>Название тренировки:</b> <i>{data["train"].name}</i>\n' +
                                    f'<b>Приоритет тренировки:</b> <i>{data["train"].priority}</i>\n' +
                                    f'<b>Время отдыха между упражнениями:</b> <i>{data["train"].rest}</i>\n' +
                                    f'<b>Упражнения:</b>\n<i>{exercisesText}</i>',
                                    user_id, data['message_id'],
                                    reply_markup=keyboard)

        data['backTexts'] = data['backTexts'][:-1]
        data['backKeyboards'] = data['backKeyboards'][:-1]
        data['backStates'] = data['backStates'][:-1]
        data['stage'] = 'choice'


# Processing commands when editing the training
async def commandsEditTraining(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    if len(message.text) > 34:
        return
    hasChanges = False

    async with state.proxy() as data:
        if data['stage'] == 'name':
            names = []
            for train in data['trainings']:
                names.append(train.name)
            if message.text in names:
                data['temp'] += 1
                await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n' +
                                            'Такая тренировка уже есть. Введите новое название (max. 34)' + (
                                                    '!' * data['temp']),
                                            message.from_user.id, data['message_id'],
                                            reply_markup=kb.cancelKeyboard)

            else:
                tr.editTraining(data["train"].id, 'name', message.text)
                data['backTexts'][-2] = data['backTexts'][-2].replace(
                    'Тренировка "' + data["train"].name + '"',
                    'Тренировка "' + message.text + '"')

                data["train"].name = message.text
                hasChanges = True

        elif data['stage'] == 'rest':
            time = tr.setsProcessing(message.text)[0]
            tr.editTraining(data["train"].id, 'rest', time)
            data["train"].rest = time
            hasChanges = True

    if hasChanges:
        await showEditedTrainingMessage(message.from_user.id, state)


# Show date of last training
async def callbackShowLastTrainingDate(callback_query: types.CallbackQuery,
                                       state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

    lastDate = tr.getLastTrainingDate(callback_query.from_user.id)

    lastDate = str(datetime.datetime.fromtimestamp(lastDate))

    keyboard = {"inline_keyboard": []}
    keyboard['inline_keyboard'].append([{'text': 'Удалить', 'callback_data': 'remove'}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Дата последней тренировки==</b>\n' + str(lastDate),
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.lastTrainingDate.set()


# Removing last training from the database
async def callbackRemoveLastTraining(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    tr.removeLastTraining(callback_query.from_user.id)

    await bot.edit_message_text('<b>==Последняя тренировка удалена==</b>\n',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.backKeyboard)


def registerHandlers(dp: Dispatcher):
    dp.register_callback_query_handler(callbackShowTrainingsForEdit, lambda c: c.data == 'trainEdit',
                                       state=Trainings.main)
    dp.register_callback_query_handler(callbackEditTraining, lambda c: c.data != 'back',
                                       state=Trainings.editTrainingSetName)
    dp.register_callback_query_handler(callbackEditTrainingName, lambda c: c.data == 'editName',
                                       state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingPriority, lambda c: c.data == 'editPriority',
                                       state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingPrioritySet, lambda c: c.data != 'back',
                                       state=Trainings.editTrainingSetPriority)
    dp.register_callback_query_handler(callbackEditTrainingRest, lambda c: c.data == 'editRest',
                                       state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingAddExe, lambda c: c.data == 'addExe',
                                       state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingAddExeChoice, lambda c: c.data != 'back',
                                       state=Trainings.editTrainingAddExe)
    dp.register_callback_query_handler(callbackEditTrainingRemoveExe, lambda c: c.data == 'removeExe',
                                       state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingRemoveExeChoice, lambda c: c.data != 'back',
                                       state=Trainings.editTrainingRemoveExe)
    dp.register_callback_query_handler(callbackEditTrainingRemoveTrain, lambda c: c.data == 'removeTrain',
                                       state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackShowLastTrainingDate, lambda c: c.data == 'lastDate',
                                       state=Trainings.main)
    dp.register_callback_query_handler(callbackRemoveLastTraining, lambda c: c.data == 'remove',
                                       state=Trainings.lastTrainingDate)
    dp.register_message_handler(commandsEditTraining, state=Trainings.editTraining)
