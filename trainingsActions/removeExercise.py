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
    trainings = tr.getTrainingList(callback_query.from_user.id)
    print(trainings)
    '''await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    m = await bot.send_message(callback_query.from_user.id,
        '<b>-=Удалить упражнение=-</b>\n\nВведите название упражнения:',
        reply_markup=kb.cancelKeyboard)
    await Trainings.addExercise.set()
    async with state.proxy() as data:
        data['stage'] = 'name'
        data['message_id'] = m.message_id'''

def registerHandlers(dp : Dispatcher):
    dp.register_callback_query_handler(callbackRemoveExercise, lambda c: c.data == 'exeRemove', state=Trainings.main)