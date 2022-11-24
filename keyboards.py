from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Global Buttons
backButton = InlineKeyboardButton('<< Назад', callback_data='back')
cancelButton = InlineKeyboardButton('<< Отменить', callback_data='back')
confirmButton = InlineKeyboardButton('>> Подтвердить <<', callback_data='confirm')
mMenuButton = InlineKeyboardButton('<< Главное меню >>', callback_data='mMenu')

# Back Keyboard
backKeyboard = InlineKeyboardMarkup().add(backButton)

# Cancel Keyboard
cancelKeyboard = InlineKeyboardMarkup().add(cancelButton)

# Confirm Keyboard
confirmKeyboard = InlineKeyboardMarkup()
confirmKeyboard.add(confirmButton)
confirmKeyboard.add(cancelButton)


# Main Menu Keyboard
trainButton = InlineKeyboardButton('Физкультура', callback_data='trainMenu')
carButton = InlineKeyboardButton('Автомобиль', callback_data='carMenu')
mMenuKeyboard = InlineKeyboardMarkup()
mMenuKeyboard.add(trainButton)
mMenuKeyboard.add(carButton)

# Train Menu Keyboard
qStartButton = InlineKeyboardButton('Быстрая тренировка', callback_data='qStart')
trainChoiceButton = InlineKeyboardButton('Выбрать тренировку', callback_data='trainChoice')
trainSettingsButton = InlineKeyboardButton('Настройки', callback_data='trainSettings')
trainMainKeyboard = InlineKeyboardMarkup()
trainMainKeyboard.add(qStartButton)
trainMainKeyboard.add(trainChoiceButton)
trainMainKeyboard.add(trainSettingsButton)
trainMainKeyboard.add(backButton)

# Train Settings Keyboard
showTrainingsButton = InlineKeyboardButton('Тренировки', callback_data='trainsShow')
showExerciseButton = InlineKeyboardButton('Упражнения', callback_data='exeShow')
trainSettingsKeyboard = InlineKeyboardMarkup()
trainSettingsKeyboard.add(showTrainingsButton)
trainSettingsKeyboard.insert(showExerciseButton)
trainSettingsKeyboard.add(backButton)
trainSettingsKeyboard.add(mMenuButton)

# Exercise Type Keyboard
repsButton = InlineKeyboardButton('Повторы', callback_data='reps')
timeButton = InlineKeyboardButton('Время', callback_data='time')
exerciseTypeKeyboard = InlineKeyboardMarkup()
exerciseTypeKeyboard.add(repsButton)
exerciseTypeKeyboard.add(timeButton)
exerciseTypeKeyboard.add(cancelButton)

# Training Priority Keyboard
highPriorityTrainButton = InlineKeyboardButton('Высокий', callback_data='Высокий')
averagePriorityTrainButton = InlineKeyboardButton('Обычный', callback_data='Обычный')
specialPriorityTrainButton = InlineKeyboardButton('Особый', callback_data='Особый')
trainPriorityKeyboard = InlineKeyboardMarkup()
trainPriorityKeyboard.add(highPriorityTrainButton)
trainPriorityKeyboard.add(averagePriorityTrainButton)
trainPriorityKeyboard.add(specialPriorityTrainButton)
trainPriorityKeyboard.add(cancelButton)


# Exercise Edit Choice Keyboard
nameButton = InlineKeyboardButton('Название', callback_data='name')
typeButton = InlineKeyboardButton('Тип', callback_data='type')
weightButton = InlineKeyboardButton('Вес', callback_data='weight')
setsButton = InlineKeyboardButton('Подходы', callback_data='sets')
restButton = InlineKeyboardButton('Отдых', callback_data='rest')
addRepsButton = InlineKeyboardButton('Прирост повторов', callback_data='add_reps')
maxButton = InlineKeyboardButton('Максимум повторов', callback_data='max')
orderButton = InlineKeyboardButton('Порядок прироста', callback_data='order')
exerciseEditKeyboard = InlineKeyboardMarkup()
exerciseEditKeyboard.insert(nameButton)
exerciseEditKeyboard.insert(typeButton)
exerciseEditKeyboard.insert(weightButton)
exerciseEditKeyboard.add(setsButton)
exerciseEditKeyboard.insert(restButton)
exerciseEditKeyboard.add(maxButton)
exerciseEditKeyboard.add(addRepsButton)
exerciseEditKeyboard.add(orderButton)
exerciseEditKeyboard.add(backButton)
exerciseEditKeyboard.add(mMenuButton)

