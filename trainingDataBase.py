import dataBase as db
import json
import datetime
import re

# Обработка строки повторов
def setsProcessing(sets):
	try:
	    sets = re.findall(r'\d+', sets)
	    for i, v in enumerate(sets):
	        sets[i] = int(sets[i])
	    return sets
	except Exception as e:
		print(e)
		return [0]

# Проверить, есть ли такое упражнение
def checkExercise(user_id, name, exeType, weight):
	db.cur.execute('''SELECT name, type, weight FROM exercises WHERE
		user_id = ? AND name = ? AND type = ? AND weight = ?''', (user_id, name, exeType, weight))
	if db.cur.fetchone():
		return True
	else:
		return False

# Добавить упражение
def addExercise(user_id, name, exeType, weight, sets, rest):
	sets = json.dumps(sets)
	db.cur.execute('''INSERT INTO exercises
		(user_id, name, type, weight, sets, rest)
		VALUES(?, ?, ?, ?, ?, ?)''', (user_id, name, exeType, weight, sets, rest))
	db.base.commit()

# Получить список упражнений
def getExerciseList(user_id):
	db.cur.execute('''SELECT name, type, weight, sets, rest, id FROM exercises WHERE user_id = ?''', (user_id,))
	trainings =  db.cur.fetchall()
	if trainings:
		for i, v in enumerate(trainings):
			trainings[i] = list(v)
		return trainings
	else:
		return False

# Удалить упражнение
def removeExercise(user_id, name, exeType, weight):
	db.cur.execute('''DELETE FROM exercises
		WHERE user_id = ? AND name = ? AND type = ? AND weight = ?''',
		(user_id, name, exeType, weight))
	db.base.commit()

# Изменить один параметр упражнения
def editExercise(exeId, param, new):
	db.cur.execute(f'UPDATE exercises SET {param} = ? WHERE id = ?',
		(new, exeId))
	db.base.commit()











