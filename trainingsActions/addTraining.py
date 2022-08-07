from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData

# Add Training    
async def callbackAddTraining(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Добавить тренировку==</b>\n\nВведите название тренировки:',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.cancelKeyboard)
    await Trainings.addTrain.set()
    async with state.proxy() as data:
        data['stage'] = 'name'

async def commandsAddTraining(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    async with state.proxy() as data:
        if data['stage'] == 'name':
            if tr.isTrainingExist(message.from_user.id, message.text):
                await bot.edit_message_text('<b>==Упражнение уже существует==</b>\n'+
                'Упражнение с таким названием уже существует.\n'+
                'Введите другое название.',
                message.from_user.id, data['message_id'],
                reply_markup=kb.cancelKeyboard)
            else:
                data['stage'] = 'priority'
                data['name'] = message.text
                await bot.edit_message_text('<b>==Добавить тренировку==</b>\n'+
                    f'<b>Название тренировки:</b> <i>{data["name"]}</i>\n\n'+
                    'Выберите приоритет тренировки:',
                    message.from_user.id, data['message_id'],
                    reply_markup=kb.trainPriorityKeyboard)
        elif data['stage'] == 'rest':
            data['stage'] = 'confirm'
            data['rest'] = tr.setsProcessing(message.text)[0]
            await bot.edit_message_text('<b>==Добавить тренировку==</b>\n'+
                f'<b>Название тренировки:</b> <i>{data["name"]}</i>\n'+
                f'<b>Приоритет тренировки:</b> <i>{data["priority"]}</i>\n'+
                f'<b>Отдых между упражнениями:</b> <i>{data["rest"]}</i>\n\n'+
                'Подтверждаете добавление тренировки?',
                message.from_user.id, data['message_id'],
                reply_markup=kb.confirmKeyboard)

async def callbackAddTrainingPriority(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        data['stage'] = 'rest'
        data['priority'] = callback_query.data
        await bot.edit_message_text('<b>==Добавить тренировку==</b>\n'+
            f'<b>Название тренировки:</b> <i>{data["name"]}</i>\n'+
            f'<b>Приоритет тренировки:</b> <i>{data["priority"]}</i>\n\n'+
            'Введите время отдыха между упражнениями:',
            callback_query.from_user.id, callback_query.message.message_id,
            reply_markup=kb.cancelKeyboard)

async def callbackAddTrainingConfirm(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.addTraining(callback_query.from_user.id, data['name'], data['priority'], data['rest'])
        data['stage'] = ''
        data['trainings'] = trainings = tr.getTrainingsList(callback_query.from_user.id)
        await bot.edit_message_text( '<b>==Тренировка добавлена==</b>\n'+
            f'<b>Название тренировки:</b> <i>{data["name"]}</i>\n'+
            f'<b>Приоритет тренировки:</b> <i>{data["priority"]}</i>\n'+
            f'<b>Отдых между упражнениями:</b> <i>{data["rest"]}</i>\n',
            callback_query.from_user.id, callback_query.message.message_id,
            reply_markup=kb.backKeyboard)

    keyboard = {"inline_keyboard": []}

    keyboard['inline_keyboard'].append([{'text': '>> Изменить тренировку', 'callback_data': 'trainEdit'}])
    keyboard['inline_keyboard'].append([{'text': '>> Добавить тренировку', 'callback_data': 'trainAdd'}])
    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
    keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])
    
    trainingsListText = ''
    for v in trainings:
        trainingsListText += f'- Тренировка "{v[0]}", приоритет "{v[1]}"\n'

    async with state.proxy() as data:
        data['backTexts'][-1] = '<b>==Список тренировок==</b>\n\n'+trainingsListText
        data['backKeyboards'][-1] = keyboard

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackAddTraining, lambda c: c.data == 'trainAdd', state=Trainings.main)
    dp.register_callback_query_handler(callbackAddTrainingPriority, lambda c: c.data == 'Высокий', state=Trainings.addTrain)
    dp.register_callback_query_handler(callbackAddTrainingPriority, lambda c: c.data == 'Низкий', state=Trainings.addTrain)
    dp.register_callback_query_handler(callbackAddTrainingConfirm, lambda c: c.data == 'confirm', state=Trainings.addTrain)
    dp.register_message_handler(commandsAddTraining, state=Trainings.addTrain)