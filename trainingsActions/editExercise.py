from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData

# Show exercise
async def callbackShowExercises(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exercises = data['exercises']

    names = []
    for i, v in  enumerate(exercises):
        if v[0] not in names:
            names.append(v[0])

    keyboard = {"inline_keyboard": []}
    for i, v in enumerate(names):
        keyboard['inline_keyboard'].append([{'text': v, 'callback_data': v}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите упражнение==</b>\n\nВыберите название упражнения:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.editExerciseName.set()
    async with state.proxy() as data:
        data['exercises'] = exercises

async def callbackEditExerciseName(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exercises = data['exercises']
        data['name'] = name = callback_query.data

    types = []
    for i, v in  enumerate(exercises):
        if v[0] == name and v[1] not in types:
            types.append(v[1])

    keyboard = {"inline_keyboard": []}
    for i, v in enumerate(types):
        keyboard['inline_keyboard'].append([{'text': ('Повторы' if v == 'reps' else 'По времени'),
        'callback_data': v}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите упражнение==</b>\n\nВыберите тип упражнения:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.editExerciseType.set()

async def callbackEditExerciseType(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exercises = data['exercises']
        data['type'] = exeType = callback_query.data
        name = data['name']

    weights = []
    for i, v in  enumerate(exercises):
        if v[0] == name and v[1] == exeType and v[2] not in weights:
            weights.append(v[2])

    keyboard = {"inline_keyboard": []}
    for i, v in enumerate(weights):
        keyboard['inline_keyboard'].append([{'text': v, 'callback_data': v}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Выберите упражнение==</b>\n\nВыберите вес:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.editExerciseWeight.set()

async def callbackEditExerciseWeight(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exeType = data['type']
        name = data['name']
        weight = data['weight'] = callback_query.data
    
    keyboard = {"inline_keyboard": []}
    keyboard['inline_keyboard'].append([{'text': 'Изменить', 'callback_data': 'edit'}])
    keyboard['inline_keyboard'].append([{'text': 'Удалить', 'callback_data': 'remove'}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])
    keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
        f'<b>Упражнение:</b> <i>{name}</i>\n'+
        f'<b>Тип:</b> <i>{"Повторы" if exeType == "reps" else "По времени"}</i>\n'+
        f'<b>Вес:</b> <i>{weight}</i>\n',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.main.set()

# Remove Exercise
async def callbackEditExerciseRemove(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.removeExercise(callback_query.from_user.id, data['name'], data['type'], data['weight'])
        data['exercises'] = exercises = tr.getExerciseList(callback_query.from_user.id)

    keyboard = {"inline_keyboard": []}

    if not(exercises):
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
        for v in exercises:
            exercisesListText += f'{v[0]} на {"повторы" if v[1] == "reps" else "время"} с весом: {v[2]}\n'

        async with state.proxy() as data:
            data['backTexts'][-1] = '<b>==Список упражнений==</b>\n\n'+exercisesListText
            data['backKeyboards'][-1] = keyboard

    await bot.edit_message_text('<b>==Упражнение удалено==</b>\n\n',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.backKeyboard)

async def callbackEditExercise(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    async with state.proxy() as data:
        i = 0
        while (data['name'] != data['exercises'][i][0] and
            data['type'] != data['exercises'][i][1] and
            data['weight'] != data['exercises'][i][2]):
            i += 1
        else:
            data['sets'] = data['exercises'][i][3]
            data['rest'] = data['exercises'][i][4]
            data['exeId'] = data['exercises'][i][5]
            data['index'] = i
            data['stage'] = 'choice'
            data['temp'] = 0
        name = data['name']
        exeType = data['type']
        weight = data['weight']
        sets = data['sets']
        rest = data['rest']

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
        f'<b>Название упражнения:</b> <i>{name}</i>\n'+
        f'<b>Тип упражнения:</b> <i>{"Повторы" if exeType=="reps" else "Время"}</i>\n'+
        f'<b>Вес:</b> <i>{weight}</i>\n'+
        f'<b>Подходы:</b> <i>{sets}</i>\n'+
        f'<b>Время отдыха между подходами:</b> <i>{rest}</i>.\n\n'+
        'Что изменить?',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.exerciseEditKeyboard)

    await Trainings.editExercise.set()

async def callbackEditExerciseNewName(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
        'Введите новое имя:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'name'

async def callbackEditExerciseNewType(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
        'Выберите тип.',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.exerciseTypeKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'type'

async def callbackEditExerciseNewWeight(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
        'Введите вес:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'weight'

async def callbackEditExerciseNewSets(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
        'Введите подходы через пробел:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'sets'

async def callbackEditExerciseNewRest(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
        'Введите время отдыха между подходами:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)

    async with state.proxy() as data:
        data['stage'] = 'rest'

async def commandsEditExercise(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    async with state.proxy() as data:
        if data['stage'] == 'name':
            newExercise = data['exercises'][data['index']].copy()
            newExercise[0] = message.text 
            if newExercise in data['exercises']:
                data['temp'] += 1
                await bot.edit_message_text('<b>==Изменить упражнение==</b>\n\n'+
                    'Такое упражнение уже есть. Введите новое имя' + ('!' * data['temp']),
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.cancelKeyboard)
            else:
                tr.editExercise(data['exeId'], 'name', message.text)
                for i, v in enumerate(data['backTexts']):
                    data['backTexts'][i] = v.replace(data['name'], message.text)

                data['name'] = message.text
                data['exercises'][data['index']] = newExercise
                await bot.edit_message_text('<b>==Упражнение изменено!==</b>\n\n'+
                    f"<b>Название упражнения:</b> <i>{data['name']}</i>\n"+
                    f"<b>Тип упражнения:</b> <i>{'Повторы' if data['type']=='reps' else 'Время'}</i>\n"+
                    f"<b>Вес:</b> <i>{data['weight']}</i>\n"+
                    f"<b>Подходы:</b> <i>{data['sets']}</i>\n"+
                    f"<b>Время отдыха между подходами:</b> <i>{data['rest']}</i>.\n\n"+
                    'Что изменить?',
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.exerciseEditKeyboard)

                data['backTexts'] = data['backTexts'][:-1]
                data['backKeyboards'] = data['backKeyboards'][:-1]
                data['backStates'] = data['backStates'][:-1]                    

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackShowExercises, lambda c: c.data == 'exeEdit', state=Trainings.main)
    dp.register_callback_query_handler(callbackEditExerciseName, lambda c: c.data != 'back', state=Trainings.editExerciseName)
    dp.register_callback_query_handler(callbackEditExerciseType, lambda c: c.data != 'back', state=Trainings.editExerciseType)
    dp.register_callback_query_handler(callbackEditExerciseWeight, lambda c: c.data != 'back', state=Trainings.editExerciseWeight)
    dp.register_callback_query_handler(callbackEditExerciseRemove, lambda c: c.data == 'remove', state=Trainings.main)
    dp.register_callback_query_handler(callbackEditExercise, lambda c: c.data == 'edit', state=Trainings.main)
    dp.register_callback_query_handler(callbackEditExerciseNewName, lambda c: c.data == 'name', state=Trainings.editExercise)
    dp.register_message_handler(commandsEditExercise, state=Trainings.editExercise)