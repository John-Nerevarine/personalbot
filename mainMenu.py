from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from support import callbackEmergencyStart
import keyboards as kb
import datetime
from createBot import MainMenu, bot
from config import USERS

# Start
async def commandStart(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    if message.from_user.id in USERS:
        m = await bot.send_message(message.from_user.id, '<b>==Главное меню==</b>',
                reply_markup=kb.mMenuKeyboard)
        await state.finish()
        await MainMenu.start.set()
        async with state.proxy() as data:
            data['backStates'] = []
            data['backTexts'] = []
            data['backKeyboards'] = []
            data['message_id'] = m.message_id
    else:
        m = await bot.send_message(message.from_user.id, '<b>==У вас нет доступа к боту==</b>')
        try:
            file =  open('unauthorized_access_log.txt', 'a')
            file.write(f'{datetime.datetime.now()} | {message.from_user.id}' +
                f' | {message.from_user.full_name} | {message.from_user.username}\n')
        finally:
            file.close()

# Return to main menu
async def callbackMainMenu(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    m = await bot.edit_message_text('<b>==Главное меню==</b>',
        callback_query.from_user.id, callback_query.message.message_id,
        reply_markup=kb.mMenuKeyboard)
    await state.finish()
    await MainMenu.start.set()
    async with state.proxy() as data:
        data['backStates'] = []
        data['backTexts'] = []
        data['backKeyboards'] = []
        data['message_id'] = m.message_id

# Back
async def getBackData(state:  FSMContext, message):
    async with state.proxy() as data:    
        data['backStates'].append(await state.get_state())
        data['backTexts'].append(message.text)
        data['backKeyboards'].append(message.reply_markup)

async def callbackGoBack(callback_query: types.CallbackQuery,
                                     state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    if await state.get_state():
        async with state.proxy() as data:
            await bot.edit_message_text(data['backTexts'][-1],
                callback_query.from_user.id, callback_query.message.message_id,
                reply_markup= data['backKeyboards'][-1])
            if data['backStates'][-1] == 'MainMenu:start':
                await state.finish()
                await MainMenu.start.set()
                data['backStates'] = []
                data['backTexts'] = []
                data['backKeyboards'] = []
            else:
                await state.set_state(data['backStates'][-1])
                data['backStates'].pop(-1)
                data['backTexts'].pop(-1)
                data['backKeyboards'].pop(-1)
    else:
        await callbackEmergencyStart(callback_query, state)
    

def registerHandlers(dp : Dispatcher):
    dp.register_message_handler(commandStart, commands=['start'], state='*')
    dp.register_callback_query_handler(callbackGoBack, lambda c: c.data == 'back', state='*')
    dp.register_callback_query_handler(callbackMainMenu, lambda c: c.data == 'mMenu', state='*')