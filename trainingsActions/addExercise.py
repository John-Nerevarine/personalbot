from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData

# Add Exercise    
async def callbackAddExercise(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Добавить упражнение==</b>\n\nВведите название упражнения:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)
    await Trainings.addExercise.set()
    async with state.proxy() as data:
        data['stage'] = 'name'

async def commandsAddExercise(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    async with state.proxy() as data:
        if data['stage'] == 'name':
            data['stage'] = 'type'
            data['name'] = message.text
            await bot.edit_message_text('<b>==Добавить упражнение==</b>\n'+
                f'<b>Название упражнения:</b> <i>{data["name"]}</i>\n\n'+
                'Выберите тип упражнения:',
                message.from_user.id, data['message_id'],
                reply_markup=kb.exerciseTypeKeyboard)

        elif data['stage'] == 'weight':
            data['stage'] = 'sets'
            data['weight'] = message.text 
            if tr.checkExercise(message.from_user.id, data['name'], data['type'], data['weight']):
                data['stage'] == 'error'
                await bot.edit_message_text('<b>==Упражнение уже существует==</b>\n'+
                'Упражнение такого типа с таким названием и весом уже существует.\n'+
                'Введите другие параметры.',
                message.from_user.id, data['message_id'],
                reply_markup={"inline_keyboard": [[{"text": "Отменить", "callback_data": "back"}],
                [{"text": "Начать заново", "callback_data": "exeAdd"}]]})
            else:
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n'+
                    f'<b>Название упражнения:</b> <i>{data["name"]}</i>\n'+
                    f'<b>Тип упражнения:</b> <i>{"Повторы" if data["type"]=="reps" else "Время"}</i>\n'+
                    f'<b>Вес:</b> <i>{data["weight"]}</i>\n\n'+
                    ('Введите количество повторов по подходам через пробел (не более пяти):' if data['type'] == 'reps'
                    else 'Введите время работы по подходам через пробел:'),
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.cancelKeyboard)

        elif data['stage'] == 'sets':
            sets = tr.setsProcessing(message.text)
            if len(sets) > 1:
                data['stage'] = 'rest'
                data['sets'] = sets
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n'+
                    f'<b>Название упражнения:</b> <i>{data["name"]}</i>\n'+
                    f'<b>Тип упражнения:</b> <i>{"Повторы" if data["type"]=="reps" else "Время"}</i>\n'+
                    f'<b>Вес:</b> <i>{data["weight"]}</i>\n'+
                    f'<b>Подходы:</b> <i>{data["sets"]}</i>\n\n'+
                    'Введите время отдыха между повторами в секундах:',
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.cancelKeyboard)

            elif len(sets) == 1:
                data['stage'] = 'confirm'
                data['sets'] = sets
                data['rest'] = False
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n'+
                    f'<b>Название упражнения:</b> <i>{data["name"]}</i>\n'+
                    f'<b>Тип упражнения:</b> <i>{"Повторы" if data["type"]=="reps" else "Время"}</i>\n'+
                    f'<b>Вес:</b> <i>{data["weight"]}</i>\n'+
                    f'<b>Подходы:</b> <i>{data["sets"]}</i>\n\n'+
                    'Подтвердите, всё верно? ',
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.confirmKeyboard)

        elif data['stage'] == 'rest':
            time = tr.setsProcessing(message.text)
            if (len(time) == 1):
                data['stage'] = 'confirm'
                data['rest'] = time[0]
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n'+
                    f'<b>Название упражнения:</b> <i>{data["name"]}</i>\n'+
                    f'<b>Тип упражнения:</b> <i>{"Повторы" if data["type"]=="reps" else "Время"}</i>\n'+
                    f'<b>Вес:</b> <i>{data["weight"]}</i>\n'+
                    f'<b>Подходы:</b> <i>{data["sets"]}</i>\n'+
                    f'<b>Время отдыха между подходами:</b> <i>{data["rest"]}</i>\n\n'+
                    'Подтвердите, всё верно?', 
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.confirmKeyboard)

async def callbackAddExerciseType(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        data['stage'] = 'weight'
        data['type'] = callback_query.data
        await bot.edit_message_text('<b>==Добавить упражнение==</b>\n'+
            f'<b>Название упражнения:</b> <i>{data["name"]}</i>\n'+
            f'<b>Тип упражнения:</b> <i>{"Повторы" if data["type"]=="reps" else "Время"}</i>\n\n'+
            'Введите снаряд и его вес:',
            callback_query.from_user.id, callback_query.message.message_id,
            reply_markup=kb.cancelKeyboard)

async def callbackAddExerciseConfirm(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.addExercise(callback_query.from_user.id, data['name'], data['type'], data['weight'],
            data['sets'], data['rest'])
        data['stage'] = ''
        data['exercises'] = exercises = tr.getExerciseList(callback_query.from_user.id)
        await bot.edit_message_text( '<b>==Упражнение добавлено==</b>\n'+
            f'<b>Название упражнения:</b> <i>{data["name"]}</i>\n'+
            f'<b>Тип упражнения:</b> <i>{"Повторы" if data["type"]=="reps" else "Время"}</i>\n'+
            f'<b>Вес:</b> <i>{data["weight"]}</i>\n'+
            f'<b>Подходы:</b> <i>{data["sets"]}</i>\n'+
            (f'<b>Время отдыха между подходами:</b> <i>{data["rest"]}</i>.' if data['rest'] else ''),
            callback_query.from_user.id, callback_query.message.message_id,
            reply_markup=kb.backKeyboard)

    keyboard = {"inline_keyboard": []}
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
            
def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackAddExercise, lambda c: c.data == 'exeAdd', state=Trainings.main)
    dp.register_callback_query_handler(callbackAddExerciseType, lambda c: c.data == 'reps', state=Trainings.addExercise)
    dp.register_callback_query_handler(callbackAddExerciseType, lambda c: c.data == 'time', state=Trainings.addExercise)
    dp.register_callback_query_handler(callbackAddExerciseConfirm, lambda c: c.data == 'confirm', state=Trainings.addExercise)
    dp.register_message_handler(commandsAddExercise, state=Trainings.addExercise)