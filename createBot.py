from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

class MainMenu(StatesGroup):
    start = State()

class Trainings(StatesGroup):
    main = State()
    #showExercises = State()
    addExercise = State()
    editExercise = State()
    editExerciseName = State()
    editExerciseType = State()
    editExerciseWeight = State()
    addTrain = State()
