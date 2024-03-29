from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import keyboards as kb
from trainingsActions import trainingDataBase as tr
from createBot import Trainings
from createBot import bot
from mainMenu import getBackData
import gym


# Start adding an exercise
async def callbackAddExercise(callback_query: types.CallbackQuery,
                              state: FSMContext):
    await getBackData(state, callback_query.message)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('<b>==Добавить упражнение==</b>\n\nВведите название упражнения (max. 34):',
                                callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.cancelKeyboard)
    await Trainings.addExercise.set()
    async with state.proxy() as data:
        data['stage'] = 'name'
        data['exe'] = gym.Exercise(user_id=callback_query.from_user.id)


# Processing commands when adding an exercise
async def commandsAddExercise(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)

    if len(message.text) > 34:
        return

    async with state.proxy() as data:
        if data['stage'] == 'name':
            data['stage'] = 'type'
            data['exe'].name = message.text
            await bot.edit_message_text('<b>==Добавить упражнение==</b>\n' +
                                        f'<b>Название упражнения:</b> <i>{data["exe"].name}</i>\n\n' +
                                        'Выберите тип упражнения:',
                                        message.from_user.id, data['message_id'],
                                        reply_markup=kb.exerciseTypeKeyboard)

        elif data['stage'] == 'weight':
            data['stage'] = 'sets'
            data['exe'].weight = message.text
            if tr.checkExercise(data['exe']):
                data['stage'] = 'error'
                await bot.edit_message_text('<b>==Упражнение уже существует==</b>\n' +
                                            'Упражнение такого типа с таким названием и весом уже существует.\n' +
                                            'Введите другие параметры.',
                                            message.from_user.id, data['message_id'],
                                            reply_markup={
                                                "inline_keyboard": [[{"text": "Отменить", "callback_data": "back"}],
                                                                    [{"text": "Начать заново",
                                                                      "callback_data": "exeAdd"}]]})
            else:
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n' +
                                            f'<b>Название упражнения:</b> <i>{data["exe"].name}</i>\n' +
                                            f'<b>Тип упражнения:</b> <i>{"Повторы" if data["exe"].type == "reps" else "Время"}</i>\n' +
                                            f'<b>Вес:</b> <i>{data["exe"].weight}</i>\n\n' +
                                            ('Введите количество повторов по подходам через пробел (не более пяти):' if
                                             data["exe"].type == 'reps'
                                             else 'Введите время работы по подходам через пробел:'),
                                            message.from_user.id, data['message_id'],
                                            reply_markup=kb.cancelKeyboard)
        elif data['stage'] == 'sets':
            sets = tr.setsProcessing(message.text)
            setsNumber = 0
            for v in sets:
                if v:
                    setsNumber += 1
            if setsNumber > 1:
                data['stage'] = 'rest'
                data['exe'].sets = sets
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n' +
                                            f'<b>Название упражнения:</b> <i>{data["exe"].name}</i>\n' +
                                            f'<b>Тип упражнения:</b> <i>{"Повторы" if data["exe"].type == "reps" else "Время"}</i>\n' +
                                            f'<b>Вес:</b> <i>{data["exe"].weight}</i>\n' +
                                            f'<b>Подходы:</b> <i>{data["exe"].sets}</i>\n\n' +
                                            'Введите время отдыха между повторами в секундах:',
                                            message.from_user.id, data['message_id'],
                                            reply_markup=kb.cancelKeyboard)

            elif setsNumber == 1:
                data['stage'] = 'confirm'
                data['exe'].sets = sets
                data['exe'].rest = 0
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n' +
                                            f'<b>Название упражнения:</b> <i>{data["exe"].name}</i>\n' +
                                            f'<b>Тип упражнения:</b> <i>{"Повторы" if data["exe"].type == "reps" else "Время"}</i>\n' +
                                            f'<b>Вес:</b> <i>{data["exe"].weight}</i>\n' +
                                            f'<b>Подходы:</b> <i>{data["exe"].sets}</i>\n\n' +
                                            'Подтвердите, всё верно? ',
                                            message.from_user.id, data['message_id'],
                                            reply_markup=kb.confirmKeyboard)
            else:
                return

        elif data['stage'] == 'rest':
            time = tr.setsProcessing(message.text)
            if time[0] > 0:
                data['stage'] = 'confirm'
                data['exe'].rest = time[0]
                await bot.edit_message_text('<b>==Добавить упражнение==</b>\n' +
                                            f'<b>Название упражнения:</b> <i>{data["exe"].name}</i>\n' +
                                            f'<b>Тип упражнения:</b> <i>{"Повторы" if data["exe"].type == "reps" else "Время"}</i>\n' +
                                            f'<b>Вес:</b> <i>{data["exe"].weight}</i>\n' +
                                            f'<b>Подходы:</b> <i>{data["exe"].sets}</i>\n' +
                                            f'<b>Время отдыха между подходами:</b> <i>{data["exe"].rest}</i>\n\n' +
                                            'Подтвердите, всё верно?',
                                            message.from_user.id, data['message_id'],
                                            reply_markup=kb.confirmKeyboard)


# Exercise type chosen
async def callbackAddExerciseType(callback_query: types.CallbackQuery,
                                  state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        data['stage'] = 'weight'
        data['exe'].type = callback_query.data
        if callback_query.data != 'reps':
            data['exe'].max_reps = 1800
            data['exe'].add_reps = 60

        await bot.edit_message_text('<b>==Добавить упражнение==</b>\n' +
                                    f'<b>Название упражнения:</b> <i>{data["exe"].name}</i>\n' +
                                    f'<b>Тип упражнения:</b> <i>{"Повторы" if data["exe"].type == "reps" else "Время"}</i>\n\n' +
                                    'Введите снаряд и его вес:',
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=kb.cancelKeyboard)


# Confirm adding an exercise
async def callbackAddExerciseConfirm(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        tr.addExercise(data['exe'])
        data['stage'] = ''
        data['exercises'] = exercises = tr.getExerciseList(callback_query.from_user.id)
        await bot.edit_message_text('<b>==Упражнение добавлено==</b>\n' +
                                    f'<b>Название упражнения:</b> <i>{data["exe"].name}</i>\n' +
                                    f'<b>Тип упражнения:</b> <i>{"Повторы" if data["exe"].type == "reps" else "Время"}</i>\n' +
                                    f'<b>Вес:</b> <i>{data["exe"].weight}</i>\n' +
                                    f'<b>Подходы:</b> <i>{data["exe"].sets}</i>\n' +
                                    (f'<b>Время отдыха между подходами:</b> <i>{data["exe"].rest}</i>.'
                                     if data['exe'].rest else ''),
                                    callback_query.from_user.id, callback_query.message.message_id,
                                    reply_markup=kb.backKeyboard)

    keyboard = {"inline_keyboard": []}
    keyboard['inline_keyboard'].append([{'text': '>> Изменить упражнение', 'callback_data': 'exeEdit'}])
    keyboard['inline_keyboard'].append([{'text': '>> Добавить упражнение', 'callback_data': 'exeAdd'}])
    keyboard['inline_keyboard'].append([{'text': '<< Назад', 'callback_data': 'back'}])
    keyboard['inline_keyboard'].append([{'text': '<< Главное меню', 'callback_data': 'mMenu'}])

    exercisesListText = ''
    for exe in exercises:
        exercisesListText += f'{exe.name} на {"повторы" if exe.type == "reps" else "время"} с весом: {exe.weight}\n'

    async with state.proxy() as data:
        data['backTexts'][-1] = '<b>==Список упражнений==</b>\n\n' + exercisesListText
        data['backKeyboards'][-1] = keyboard


def registerHandlers(dp: Dispatcher):
    dp.register_callback_query_handler(callbackAddExercise, lambda c: c.data == 'exeAdd', state=Trainings.main)
    dp.register_callback_query_handler(callbackAddExerciseType, lambda c: c.data == 'reps', state=Trainings.addExercise)
    dp.register_callback_query_handler(callbackAddExerciseType, lambda c: c.data == 'time', state=Trainings.addExercise)
    dp.register_callback_query_handler(callbackAddExerciseConfirm, lambda c: c.data == 'confirm',
                                       state=Trainings.addExercise)
    dp.register_message_handler(commandsAddExercise, state=Trainings.addExercise)
