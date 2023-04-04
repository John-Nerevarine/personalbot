from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import gym
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData
import json


# Show menu from existing exercises
async def callbackShowExercises(callback_query: types.CallbackQuery,
                                state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exercises = data['exercises']

    names = []
    for exe in exercises:
        if exe.name not in names:
            names.append(exe.name)

    keyboard = {"inline_keyboard": []}
    for name in names:
        keyboard['inline_keyboard'].append([{'text': name, 'callback_data': name}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите упражнение==</b>\n\nВыберите название упражнения:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.editExerciseName.set()


# Show existing types for the exercise
async def callbackEditExerciseName(callback_query: types.CallbackQuery,
                                   state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exercises = data['exercises']
        data['exe'] = gym.Exercise(name=callback_query.data, user_id=callback_query.from_user.id)
        name = data['exe'].name

    exe_types = []
    for exe in exercises:
        if exe.name == name and exe.type not in exe_types:
            exe_types.append(exe.type)

    keyboard = {"inline_keyboard": []}

    for exe_type in exe_types:
        keyboard['inline_keyboard'].append([{'text': ('Повторы' if exe_type == 'reps' else 'По времени'),
                                             'callback_data': exe_type}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите упражнение==</b>\n\nВыберите тип упражнения:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.editExerciseType.set()


# Show existing weights for the exercise
async def callbackEditExerciseType(callback_query: types.CallbackQuery,
                                   state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exercises = data['exercises']
        data['exe'].type = exeType = callback_query.data
        name = data['exe'].name

    weights = []
    for exe in exercises:
        if exe.name == name and exe.type == exeType and exe.weight not in weights:
            weights.append(exe.weight)

    keyboard = {"inline_keyboard": []}
    for weight in weights:
        keyboard['inline_keyboard'].append([{'text': weight, 'callback_data': weight}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите упражнение==</b>\n\nВыберите вес:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.editExerciseWeight.set()


# Show available actions for the exercise
async def callbackEditExerciseWeight(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exeType = data['exe'].type
        name = data['exe'].name
        weight = data['exe'].weight = callback_query.data

    keyboard = {"inline_keyboard": []}
    keyboard['inline_keyboard'].append([{'text': 'Изменить', 'callback_data': 'edit'}])
    keyboard['inline_keyboard'].append([{'text': 'Удалить', 'callback_data': 'remove'}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])
    keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                f'<b>Упражнение:</b> <i>{name}</i>\n' +
                                f'<b>Тип:</b> <i>{"Повторы" if exeType == "reps" else "По времени"}</i>\n' +
                                f'<b>Вес:</b> <i>{weight}</i>\n',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=keyboard)

    await Trainings.main.set()


# Remove the exercise
async def callbackEditExerciseRemove(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        trainsWithExercise = tr.getTrainsWithExercise(data['exe'])
        if trainsWithExercise:
            trainsText = ''
            for train in trainsWithExercise:
                trainsText += f'"{train[0]}", '
            trainsText = trainsText[:-2] + '.'
            await bot.edit_message_text('<b>==Невозможно удалить==</b>\n\n' +
                                        f'Упражнение используется в следующих тренировках: {trainsText}',
                                        callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=kb.backKeyboard)
            return

        tr.removeExercise(data['exe'])
        data['exercises'] = exercises = tr.getExerciseList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if not exercises:
        keyboard['inline_keyboard'].append([{'text': '>> Добавить упражнение', 'callback_data': 'exeAdd'}])
        keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
        keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

        async with state.proxy() as data:
            data['backTexts'][-1] = '<b>==Нет упражнений==</b>'
            data['backKeyboards'][-1] = keyboard

    else:
        keyboard['inline_keyboard'].append([{'text': '>> Изменить упражнение', 'callback_data': 'exeEdit'}])
        keyboard['inline_keyboard'].append([{'text': '>> Добавить упражнение', 'callback_data': 'exeAdd'}])
        keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
        keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

        exercisesListText = ''
        exercisesList = []
        for exe in exercises:
            if exe.name not in exercisesList:
                exercisesList.append(exe.name)
                exercisesListText += f'> {exe.name} на {"повторы" if exe.type == "reps" else "время"}\n'

        async with state.proxy() as data:
            data['backTexts'][-1] = '<b>==Список упражнений==</b>\n\n' + exercisesListText
            data['backKeyboards'][-1] = keyboard

    await bot.edit_message_text('<b>==Упражнение удалено==</b>\n\n',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.backKeyboard)


# Show available editing options for the exercise
async def callbackEditExercise(callback_query: types.CallbackQuery,
                               state: FSMContext):
    await getBackData(state, callback_query.message)
    async with state.proxy() as data:
        i = 0
        while not (data['exe'].name == data['exercises'][i].name and
                   data['exe'].type == data['exercises'][i].type and
                   data['exe'].weight == data['exercises'][i].weight):
            i += 1
        else:
            data['exe'] = data['exercises'][i]
            data['stage'] = 'choice'
            data['temp'] = 0
        exe = data['exe']

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                f'<b>Название упражнения:</b> <i>{exe.name}</i>\n' +
                                f'<b>Тип упражнения:</b> <i>{"Повторы" if exe.type == "reps" else "Время"}</i>\n' +
                                f'<b>Вес:</b> <i>{exe.weight}</i>\n' +
                                f'<b>Подходы:</b> <i>{exe.sets}</i>\n' +
                                f'<b>Время отдыха между подходами:</b> <i>{exe.rest}</i>.\n' +
                                f'<b>Прирост повторов:</b> <i>{exe.add_reps}</i>\n' +
                                f'<b>Максимум повторов:</b> <i>{exe.max_reps}</i>\n' +
                                f'<b>Очерёдность подходов:</b> <i>{exe.add_order}</i>\n\n' +
                                'Что изменить?',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.exerciseEditKeyboard)

    await Trainings.editExercise.set()


# Entering new name for the exercise
async def callbackEditExerciseNewName(callback_query: types.CallbackQuery,
                                      state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Введите новое имя (max. 34):',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'name'


# Choosing new type for the exercise
async def callbackEditExerciseNewType(callback_query: types.CallbackQuery,
                                      state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Выберите тип.',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.exerciseTypeKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'type'


# Entering new weight for the exercise
async def callbackEditExerciseNewWeight(callback_query: types.CallbackQuery,
                                        state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Введите вес (max. 34):',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'weight'


# Entering new sets for the exercise
async def callbackEditExerciseNewSets(callback_query: types.CallbackQuery,
                                      state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Введите подходы через пробел (не более пяти):',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'sets'


# Entering new rest time for the exercise
async def callbackEditExerciseNewRest(callback_query: types.CallbackQuery,
                                      state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Введите время отдыха между подходами:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'rest'


# Entering new maximum reps for the exercise
async def callbackEditExerciseNewMax(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Введите новое максимальное число повторов:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'max_reps'


# Entering new additional reps for the exercise
async def callbackEditExerciseNewAdd(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Введите Прирост числа повторов:',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'add_reps'


# Entering new reps order for the exercise
async def callbackEditExerciseNewOrder(callback_query: types.CallbackQuery,
                                       state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                'Введите новый порядок повторов в формате "0 1 2 3 4":',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'order'


# Show message with edited exercise
async def showEditedExerciseMessage(user_id, keyboard, state: FSMContext):
    async with state.proxy() as data:
        await bot.edit_message_text('<b>==Упражнение изменено!==</b>\n\n' +
                                    f"<b>Название упражнения:</b> <i>{data['exe'].name}</i>\n" +
                                    f"<b>Тип упражнения:</b> <i>{'Повторы' if data['exe'].type == 'reps' else 'Время'}</i>\n" +
                                    f"<b>Вес:</b> <i>{data['exe'].weight}</i>\n" +
                                    f"<b>Подходы:</b> <i>{data['exe'].sets}</i>\n" +
                                    f"<b>Время отдыха между подходами:</b> <i>{data['exe'].rest}</i>.\n" +
                                    f"<b>Прирост повторов:</b> <i>{data['exe'].add_reps}</i>\n" +
                                    f"<b>Максимум повторов:</b> <i>{data['exe'].max_reps}</i>\n" +
                                    f"<b>Очерёдность подходов:</b> <i>{data['exe'].add_order}</i>\n\n" +
                                    "Что изменить?",
                                    user_id, data['message_id'],
                                    reply_markup=keyboard)
        data['stage'] = 'choice'


# Set new exercise type
async def callbackEditExerciseNewTypeSet(callback_query: types.CallbackQuery,
                                         state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        newExercise = data['exe'].copy()
        newExercise.type = callback_query.data
        if newExercise in data['exercises']:
            data['temp'] += 1
            await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                        'Такое упражнение уже есть. Выберите другой тип' + ('!' * data['temp']),
                                        callback_query.from_user.id, data['message_id'],
                                        reply_markup=kb.cancelKeyboard)
            return
        else:
            tr.editExercise(newExercise.id, 'type', callback_query.data)
            if callback_query.data == 'reps':
                data['backTexts'][-2] = data['backTexts'][-2].replace('Тип: По времени', 'Тип: Повторы')
                data['backTexts'][-3] = data['backTexts'][-3].replace(data['exe'].name +
                                                                      ' на время с весом: ' + data['exe'].weight,
                                                                      data['exe'].name +
                                                                      ' на повторы с весом: ' + data['exe'].weight)

            else:
                data['backTexts'][-2] = data['backTexts'][-2].replace('Тип: Повторы', 'Тип: По времени')
                data['backTexts'][-3] = data['backTexts'][-3].replace(data['exe'].name +
                                                                      ' на повторы с весом: ' + data['exe'].weight,
                                                                      data['exe'].name +
                                                                      ' на время с весом: ' + data['exe'].weight)

            data['exe'].type = callback_query.data
            data['backTexts'] = data['backTexts'][:-1]
            data['backKeyboards'] = data['backKeyboards'][:-1]
            data['backStates'] = data['backStates'][:-1]

    await showEditedExerciseMessage(callback_query.from_user.id, kb.exerciseEditKeyboard, state)


# Processing commands when editing the exercise
async def commandsEditExercise(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    if len(message.text) > 34:
        return
    hasChanges = False

    async with state.proxy() as data:
        if data['stage'] == 'name':
            newExercise = data['exe'].copy()
            newExercise.name = message.text
            if newExercise in data['exercises']:
                data['temp'] += 1
                await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                            'Такое упражнение уже есть. Введите новое имя' + ('!' * data['temp']),
                                            message.from_user.id, data['message_id'],
                                            reply_markup=kb.cancelKeyboard)

            else:
                tr.editExercise(newExercise.id, 'name', message.text)
                data['backTexts'][-2] = data['backTexts'][-2].replace('Упражнение: ' + data['exe'].name,
                                                                      'Упражнение: ' + message.text)
                data['backTexts'][-3] = data['backTexts'][-3].replace(data['exe'].name +
                                                                      (' на время с весом: ' if data['exe'].type == 'time' else ' на повторы с весом: ') +
                                                                      data['exe'].weight, message.text +
                                                                      (' на время с весом: ' if data['exe'].type == 'time' else ' на повторы с весом: ') +
                                                                      data['exe'].weight)

                data['exe'].name = message.text
                data['backTexts'] = data['backTexts'][:-1]
                data['backKeyboards'] = data['backKeyboards'][:-1]
                data['backStates'] = data['backStates'][:-1]
                hasChanges = True

        elif data['stage'] == 'weight':
            newExercise = data['exe'].copy()
            newExercise.weight = message.text
            if newExercise in data['exercises']:
                data['temp'] += 1
                await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n' +
                                            'Такое упражнение уже есть. Введите новый вес' + ('!' * data['temp']),
                                            message.from_user.id, data['message_id'],
                                            reply_markup=kb.cancelKeyboard)

            else:
                tr.editExercise(newExercise.id, 'weight', message.text)
                data['backTexts'][-2] = data['backTexts'][-2].replace('Вес: ' + data['exe'].weight,
                                                                      'Вес: ' + message.text)
                data['backTexts'][-3] = data['backTexts'][-3].replace(data['exe'].name +
                                                                      (' на время с весом: ' if data['exe'].type == 'time' else ' на повторы с весом: ') +
                                                                      data['exe'].weight, data['exe'].name +
                                                                      (' на время с весом: ' if data['exe'].type == 'time' else ' на повторы с весом: ') +
                                                                      message.text)

                data['exe'].weight = message.text
                data['backTexts'] = data['backTexts'][:-1]
                data['backKeyboards'] = data['backKeyboards'][:-1]
                data['backStates'] = data['backStates'][:-1]
                hasChanges = True

        elif data['stage'] == 'sets':
            data['exe'].sets = tr.setsProcessing(message.text)
            tr.editExercise(data['exe'].id, 'sets', json.dumps(data['exe'].sets))
            data['backTexts'] = data['backTexts'][:-1]
            data['backKeyboards'] = data['backKeyboards'][:-1]
            data['backStates'] = data['backStates'][:-1]
            hasChanges = True

        elif data['stage'] == 'rest':
            data['exe'].rest = tr.setsProcessing(message.text)[0]
            tr.editExercise(data['exe'].id, 'rest', data['exe'].rest)
            data['backTexts'] = data['backTexts'][:-1]
            data['backKeyboards'] = data['backKeyboards'][:-1]
            data['backStates'] = data['backStates'][:-1]
            hasChanges = True

        elif data['stage'] == 'max_reps':
            data['exe'].max_reps = tr.setsProcessing(message.text)[0]
            tr.editExercise(data['exe'].id, 'max_reps', data['exe'].max_reps)
            data['backTexts'] = data['backTexts'][:-1]
            data['backKeyboards'] = data['backKeyboards'][:-1]
            data['backStates'] = data['backStates'][:-1]
            hasChanges = True

        elif data['stage'] == 'add_reps':
            data['exe'].add_reps = tr.setsProcessing(message.text)[0]
            tr.editExercise(data['exe'].id, 'add_reps', data['exe'].add_reps)
            data['backTexts'] = data['backTexts'][:-1]
            data['backKeyboards'] = data['backKeyboards'][:-1]
            data['backStates'] = data['backStates'][:-1]
            hasChanges = True

        elif data['stage'] == 'order':
            data['exe'].add_order = tr.setsProcessing(message.text)
            tr.editExercise(data['exe'].id, 'add_order', json.dumps(data['exe'].add_order))
            data['backTexts'] = data['backTexts'][:-1]
            data['backKeyboards'] = data['backKeyboards'][:-1]
            data['backStates'] = data['backStates'][:-1]
            hasChanges = True

    if hasChanges:
        await showEditedExerciseMessage(message.from_user.id, kb.exerciseEditKeyboard, state)


def registerHandlers(dp: Dispatcher):
    dp.register_callback_query_handler(callbackShowExercises, lambda c: c.data == 'exeEdit', state=Trainings.main)
    dp.register_callback_query_handler(callbackEditExerciseName, lambda c: c.data != 'back',
                                       state=Trainings.editExerciseName)
    dp.register_callback_query_handler(callbackEditExerciseType, lambda c: c.data != 'back',
                                       state=Trainings.editExerciseType)
    dp.register_callback_query_handler(callbackEditExerciseWeight, lambda c: c.data != 'back',
                                       state=Trainings.editExerciseWeight)
    dp.register_callback_query_handler(callbackEditExerciseRemove, lambda c: c.data == 'remove', state=Trainings.main)
    dp.register_callback_query_handler(callbackEditExercise, lambda c: c.data == 'edit', state=Trainings.main)
    dp.register_callback_query_handler(callbackEditExerciseNewName, lambda c: c.data == 'name',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewType, lambda c: c.data == 'type',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewWeight, lambda c: c.data == 'weight',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewSets, lambda c: c.data == 'sets',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewRest, lambda c: c.data == 'rest',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewMax, lambda c: c.data == 'max',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewAdd, lambda c: c.data == 'add_reps',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewOrder, lambda c: c.data == 'order',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewTypeSet, lambda c: c.data == 'reps',
                                       state=Trainings.editExercise)
    dp.register_callback_query_handler(callbackEditExerciseNewTypeSet, lambda c: c.data == 'time',
                                       state=Trainings.editExercise)
    dp.register_message_handler(commandsEditExercise, state=Trainings.editExercise)
