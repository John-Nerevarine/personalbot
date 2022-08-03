from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData
import json

# Show exercise
async def callbackShowTrainings(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        trainings = data['trainings']

    keyboard = {"inline_keyboard": []}
    for i, v in enumerate(trainings):
        keyboard['inline_keyboard'].append([{'text': v[0], 'callback_data': i}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите тренировку==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.editTrainingSetName.set()

async def callbackEditTraining(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    i = int(callback_query.data)
    async with state.proxy() as data:
        name = data['trainings'][i][0]
        priority = data['trainings'][i][1]
        rest =data['trainings'][i][2]
        data['i'] = i
        data['exercisesInTrain'] = exercisesInTrain = tr.getExercisesInTrain(data['trainings'][i][3])
        data['stage'] = 'choice'
        data['temp'] = 0

    keyboard = {"inline_keyboard": []}
    keyboard['inline_keyboard'].append([{'text': 'Изменить название', 'callback_data': 'editName'}])
    keyboard['inline_keyboard'].append([{'text': 'Изменить приоритет', 'callback_data': 'editPriority'}])
    keyboard['inline_keyboard'].append([{'text': 'Изменить время отдыха', 'callback_data': 'editRest'}])
    keyboard['inline_keyboard'].append([{'text': 'Добавить упражнение', 'callback_data': 'addExe'}])
    
    exercisesText = ''
    if exercisesInTrain:
        for v in exercisesInTrain:
            exercisesText += v +'\n'
        keyboard['inline_keyboard'].append([{'text': 'Удалить упражнение', 'callback_data': 'removeExe'}])
    else:
    	exercisesText = 'В тренировке нет упражнений.'

    keyboard['inline_keyboard'].append([{'text': 'Удалить тренировку', 'callback_data': 'removeTrain'}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n'+
        f'<b>Название тренировки:</b> <i>{name}</i>\n'+
        f'<b>Приоритет тренировки:</b> <i>{priority}</i>\n'+
        f'<b>Время отдыха между упражнениями:</b> <i>{rest}</i>\n'+
        f'<b>Упражнения:</b>\n<i>{exercisesText}</i>\n',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.editTraining.set()

async def callbackEditTrainingName(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n'+
        'Введите новое название:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'name'

async def callbackEditTrainingPriority(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n'+
        'Выберите приоритет.',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.trainPriorityKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'priority'

    await Trainings.editTrainingSetPriority.set()

async def callbackEditTrainingPrioritySet(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.editTraining(data['trainings'][data['i']][3], 'priority', callback_query.data)

        data['backTexts'][-2] = data['backTexts'][-2].replace(
            'Тренировка "'+ data['trainings'][data['i']][0] + '", приоритет "'+ data['trainings'][data['i']][1] + '"',
            'Тренировка "'+ data['trainings'][data['i']][0] + '", приоритет "'+ callback_query.data + '"')

        data['trainings'][data['i']][1] = callback_query.data

    await showEditedTrainingMessage(callback_query.from_user.id, state)
    await Trainings.editTraining.set()

async def callbackEditTrainingRest(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n'+
        'Введите время отдыха:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'rest'

async def callbackEditTrainingAddExe(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    exercises = tr.getExerciseList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if not(exercises):
        keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])

        await bot.edit_message_text('<b>==Нет упражнений==</b>',
            callback_query.from_user.id, callback_query.message.message_id,
            reply_markup=keyboard)
        return

    names = []
    for v in exercises:
        if v[0] not in names:
            names.append(v[0])

    for v in names:
        keyboard['inline_keyboard'].append([{'text': v, 'callback_data': v}])

    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n'+
        'Ввыберите упражнение, которое хотите добавить:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.editTrainingAddExe.set()

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
            tr.addExerciseInTrain(data['trainings'][data['i']][3], callback_query.data)
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

async def showEditedTrainingMessage(user_id, state: FSMContext):
    async with state.proxy() as data:
        keyboard = {"inline_keyboard": []}
        keyboard['inline_keyboard'].append([{'text': 'Изменить название', 'callback_data': 'editName'}])
        keyboard['inline_keyboard'].append([{'text': 'Изменить приоритет', 'callback_data': 'editPriority'}])
        keyboard['inline_keyboard'].append([{'text': 'Изменить время отдыха', 'callback_data': 'editRest'}])
        keyboard['inline_keyboard'].append([{'text': 'Добавить упражнение', 'callback_data': 'addExe'}])

        exercisesText = ''
        if data['exercises']:
            for i, v in enumerate(data['exercises']):
                exercisesText += str(i)+'\n'
            keyboard['inline_keyboard'].append([{'text': 'Удалить упражнение', 'callback_data': 'removeExe'}])
        else:
            exercisesText = 'В тренировке нет упражнений.'

        keyboard['inline_keyboard'].append([{'text': 'Удалить тренировку', 'callback_data': 'removeTrain'}])
        keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

        await bot.edit_message_text('<b>==Тренировка изменена!==</b>\n\n'+
            f'<b>Название тренировки:</b> <i>{data["trainings"][data["i"]][0]}</i>\n'+
            f'<b>Приоритет тренировки:</b> <i>{data["trainings"][data["i"]][1]}</i>\n'+
            f'<b>Время отдыха между упражнениями:</b> <i>{data["trainings"][data["i"]][2]}</i>\n'+
            f'<b>Упражнения:</b>\n<i>{exercisesText}</i>',
            user_id, data['message_id'],
            reply_markup=keyboard)

        data['backTexts'] = data['backTexts'][:-1]
        data['backKeyboards'] = data['backKeyboards'][:-1]
        data['backStates'] = data['backStates'][:-1]
        data['stage'] = 'choice'

async def commandsEditTraining(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    hasChanges = False

    async with state.proxy() as data:
        if data['stage'] == 'name':
            names = []
            for v in data['trainings']:
                names.append(v[0])
            if message.text in names:
                data['temp'] += 1
                await bot.edit_message_text('<b>==Изменить тренировку==</b>\n\n'+
                    'Такая тренировка уже есть. Введите новое название' + ('!' * data['temp']),
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.cancelKeyboard)

            else:
                tr.editTraining(data['trainings'][data['i']][3], 'name', message.text)
                data['backTexts'][-2] = data['backTexts'][-2].replace(
                    'Тренировка "'+ data['trainings'][data['i']][0] + '"',
                    'Тренировка "'+ message.text + '"')

                data['trainings'][data['i']][0] = message.text
                hasChanges = True

        elif data['stage'] == 'rest':
            time = tr.setsProcessing(message.text)[0]
            tr.editTraining(data['trainings'][data['i']][3], 'rest', time)
            data['trainings'][data['i']][0] = time
            hasChanges = True

    if hasChanges:
        await showEditedTrainingMessage(message.from_user.id, state)

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackShowTrainings, lambda c: c.data == 'trainEdit', state=Trainings.main)
    dp.register_callback_query_handler(callbackEditTraining, lambda c: c.data != 'back', state=Trainings.editTrainingSetName)
    dp.register_callback_query_handler(callbackEditTrainingName, lambda c: c.data == 'editName', state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingPriority, lambda c: c.data == 'editPriority', state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingPrioritySet, lambda c: c.data != 'back', state=Trainings.editTrainingSetPriority)
    dp.register_callback_query_handler(callbackEditTrainingRest, lambda c: c.data == 'editRest', state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingAddExe, lambda c: c.data == 'addExe', state=Trainings.editTraining)
    dp.register_callback_query_handler(callbackEditTrainingAddExeChoice, lambda c: c.data != 'back', state=Trainings.editTrainingAddExe)
    dp.register_message_handler(commandsEditTraining, state=Trainings.editTraining)