from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData

# Remove exercise
async def callbackRemoveExercise(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    exercises = tr.getExerciseList(callback_query.from_user.id)

    if not(exercises):
        await bot.edit_message_text('<b>==Нет упражнений==</b>\n\nУпражнения не найдены.',
            callback_query.from_user.id, callback_query.message.message_id,
            reply_markup=kb.backKeyboard)
        return

    names = []
    for i, v in  enumerate(exercises):
        if v[0] not in names:
            names.append(v[0])

    keyboard = {"inline_keyboard": []}
    for i, v in enumerate(names):
        keyboard['inline_keyboard'].append([{'text': '- ' + v, 'callback_data': v}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Удалить упражнение==</b>\n\nВыберите упражнение:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.removeExerciseName.set()
    async with state.proxy() as data:
        data['exercises'] = exercises

async def callbackRemoveExerciseName(callback_query: types.CallbackQuery,
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
        keyboard['inline_keyboard'].append([{'text': '- ' + ('Повторы' if v == 'reps' else 'По времени'),
        'callback_data': v}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Удалить упражнение==</b>\n\nВыберите тип упражнения:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.removeExerciseType.set()

async def callbackRemoveExerciseType(callback_query: types.CallbackQuery,
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
        keyboard['inline_keyboard'].append([{'text': '- ' + v, 'callback_data': v}])
    keyboard['inline_keyboard'].append([{'text': '<< Отменить', 'callback_data': 'back'}])

    await bot.edit_message_text('<b>==Удалить упражнение==</b>\n\nВыберите вес:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=keyboard)

    await Trainings.removeExerciseWeight.set()

async def callbackRemoveExerciseWeight(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        exeType = data['type']
        name = data['name']
        weight = data['weight'] = callback_query.data

    await bot.edit_message_text('<b>==Подтвердите удаление==</b>\n\n'+
        f'<b>Упражнение:</b> <i>{name}</i>\n'+
        f'<b>Тип:</b> <i>{"Повторы" if exeType == "reps" else "По времени"}</i>\n'+
        f'<b>Вес:</b> <i>{weight}</i>\n',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.confirmKeyboard)

    await Trainings.main.set()

async def callbackRemoveExerciseConfirm(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.removeExercise(data['name'], data['type'], data['weight'])

    await bot.edit_message_text('<b>==Упражнение удалено==</b>\n\n',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.backKeyboard)

    await Trainings.main.set()

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackRemoveExercise, lambda c: c.data == 'exeRemove', state=Trainings.main)
    dp.register_callback_query_handler(callbackRemoveExerciseName, lambda c: c.data != 'back', state=Trainings.removeExerciseName)
    dp.register_callback_query_handler(callbackRemoveExerciseType, lambda c: c.data != 'back', state=Trainings.removeExerciseType)
    dp.register_callback_query_handler(callbackRemoveExerciseWeight, lambda c: c.data != 'back', state=Trainings.removeExerciseWeight)
    dp.register_callback_query_handler(callbackRemoveExerciseConfirm, lambda c: c.data == 'confirm', state=Trainings.main)