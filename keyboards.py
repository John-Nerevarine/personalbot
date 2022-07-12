from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Global
backButton = InlineKeyboardButton('Назад', callback_data='back')
cancelButton = InlineKeyboardButton('Отменить', callback_data='back')
confirmButton = InlineKeyboardButton('Подтвердить', callback_data='confirm')
mMenuButton = InlineKeyboardButton('Главное меню', callback_data='mMenu')

backKeyboard = InlineKeyboardMarkup().add(backButton)

cancelKeyboard = InlineKeyboardMarkup()
cancelKeyboard.add(cancelButton)

confirmKeyboard = InlineKeyboardMarkup()
confirmKeyboard.add(confirmButton)
confirmKeyboard.add(cancelButton)


# MMenu
trainButton = InlineKeyboardButton('Физкультура', callback_data='trainMenu')
carButton = InlineKeyboardButton('Автомобиль', callback_data='carMenu')
mMenuKeyboard = InlineKeyboardMarkup()
mMenuKeyboard.add(trainButton)
mMenuKeyboard.add(carButton)

# Train Menu
qStartButton = InlineKeyboardButton('Быстрая тренировка', callback_data='qStart')
trainChoiceButton = InlineKeyboardButton('Выбрать тренировку', callback_data='trainChoice')
trainSettingsButton = InlineKeyboardButton('Настройки', callback_data='trainSettings')
trainMainKeyboard = InlineKeyboardMarkup()
trainMainKeyboard.add(qStartButton)
trainMainKeyboard.add(trainChoiceButton)
trainMainKeyboard.add(trainSettingsButton)
trainMainKeyboard.add(backButton)

#Train Settings
showTrainingsButton = InlineKeyboardButton('Показать список тренировок', callback_data='trainShow')
addTrainButton = InlineKeyboardButton('Добавить тренировку', callback_data='trainAdd')
removeTrainButton = InlineKeyboardButton('Удалить тренировку', callback_data='trainRemove')
showExerciseButton = InlineKeyboardButton('Показать список упражнений', callback_data='exeShow')
addExerciseButton = InlineKeyboardButton('Добавить упражнение', callback_data='exeAdd')
removeExerciseButton = InlineKeyboardButton('Удалить упражнение', callback_data='exeRemove')
trainSettingsKeyboard = InlineKeyboardMarkup()
trainSettingsKeyboard.add(showTrainingsButton)
trainSettingsKeyboard.add(addTrainButton)
trainSettingsKeyboard.add(removeTrainButton)
trainSettingsKeyboard.add(showExerciseButton)
trainSettingsKeyboard.add(addExerciseButton)
trainSettingsKeyboard.add(removeExerciseButton)
trainSettingsKeyboard.add(backButton)
trainSettingsKeyboard.add(mMenuButton)

# Exercise Add
repsButton = InlineKeyboardButton('Повторы', callback_data='reps')
timeButton = InlineKeyboardButton('Время', callback_data='time')
exerciseTypeKeyboard = InlineKeyboardMarkup()
exerciseTypeKeyboard.add(repsButton)
exerciseTypeKeyboard.add(timeButton)
exerciseTypeKeyboard.add(cancelButton)