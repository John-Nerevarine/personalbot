import dataBase as db
import json
import datetime, time
import pygsheets
import re
from config import GS_KEY, SPSHEET

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
	exercises =  db.cur.fetchall()
	if exercises:
		for i, v in enumerate(exercises):
			exercises[i] = list(v)
		return exercises
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

def getTrainingsList(user_id):
	db.cur.execute('''SELECT name, priority, rest, id FROM trainings WHERE user_id = ?''', (user_id,))
	trainings =  db.cur.fetchall()
	if trainings:
		for i, v in enumerate(trainings):
			trainings[i] = list(v)
		return trainings
	else:
		return False

def isTrainingExist(user_id, name):
	db.cur.execute('''SELECT name FROM trainings WHERE
		user_id = ? AND name = ?''', (user_id, name))
	if db.cur.fetchone():
		return True
	else:
		return False

def addTraining(user_id, name, priority, rest):
	db.cur.execute('''INSERT INTO trainings
		(user_id, name, priority, rest)
		VALUES(?, ?, ?, ?)''', (user_id, name, priority, rest))
	db.base.commit()

def getExercisesInTrain(train_id):
	db.cur.execute('''SELECT exercise_name FROM trainings_consist WHERE
		training_id = ?''', (train_id,))
	select = db.cur.fetchall()
	ret = []
	for v in select:
		ret.append(v[0])
	return ret

def editTraining(trainId, param, new):
	db.cur.execute(f'UPDATE trainings SET {param} = ? WHERE id = ?',
		(new, trainId))
	db.base.commit()

def addExerciseInTrain(train, exe):
	db.cur.execute('''INSERT INTO trainings_consist
		(training_id, exercise_name)
		VALUES(?, ?)''', (train, exe))
	db.base.commit()

def removeExerciseFromTrain(train_id, exe):
	db.cur.execute('''DELETE FROM trainings_consist
		WHERE training_id = ? AND exercise_name = ?''',
		(train_id, exe))
	db.base.commit()

def removeTraining(train_id):
	db.cur.execute('''DELETE FROM trainings_consist
		WHERE training_id = ?''',
		(train_id,))
	db.cur.execute('''DELETE FROM trainings
		WHERE id = ?''',
		(train_id,))
	db.base.commit()

def getActualTrainingExerciseList(train_id):
	db.cur.execute('''SELECT exercises.id, name, type, weight, sets, rest FROM exercises JOIN
		trainings_consist ON name = exercise_name where training_id = ?
		GROUP BY name HAVING last = MIN(last) ORDER BY trainings_consist.id ASC''', (train_id,))
	select = db.cur.fetchall()
	if select:
		return select
	else: return False

def pushDataToSheets(user):
	db.cur.execute('''SELECT train_date FROM days
		WHERE user_id = ?
		GROUP BY user_id HAVING train_date = MAX(train_date)''', (user,))
	last_train = db.cur.fetchone()
	if not(last_train):
		last_train = 0
	else: last_train = last_train[0]

	ts = time.time()
	currentYear = 2024
	#currentYear = datetime.datetime.fromtimestamp(ts).year
	currentMonth = datetime.datetime.fromtimestamp(ts).month
	currentDay = datetime.datetime.fromtimestamp(ts).day
	lastYear = datetime.datetime.fromtimestamp(last_train).year
	lastMonth = datetime.datetime.fromtimestamp(last_train).month
	lastDay = datetime.datetime.fromtimestamp(last_train).day

	client = pygsheets.authorize(service_account_file=GS_KEY)
	spreadsht = client.open(SPSHEET)

	workSheetName = f'{currentMonth}.{currentYear}'

	if currentYear > lastYear or currentMonth > lastMonth:
		lastDay = 0
		spreadsht.add_worksheet(workSheetName)
		worksht = spreadsht.worksheet_by_title(workSheetName)
		worksht.index = 0
		worksht.update_values(crange= 'A1:H1', values=[['Дата', 'Упражнение', 'I', 'II', 'III', 'IV', 'V', 'Всего']])
		modelCell = pygsheets.Cell("A1")
		modelCell.color = (1, 0.85, 0.4, 0)
		modelCell.set_text_format('bold', True)
		rng = pygsheets.datarange.DataRange(start='A1', end='H1', worksheet=worksht)
		rng.apply_format(modelCell)
		rng.update_borders(top=True,
		                   right=True,
		                   bottom=True,
		                   left=True,
		                   inner_horizontal=True,
		                   inner_vertical=True,
		                   style='SOLID')
		worksht.adjust_column_width(start=3, end=7, pixel_size=23)

	else: 
		worksht = spreadsht.worksheet_by_title(workSheetName)

def playTraining(train_id, exercises_list, user):
	ts = time.time()
	db.cur.execute(f'UPDATE trainings SET last = ? WHERE id = ?',
		(ts, train_id))

	db.cur.execute('''INSERT INTO days (user_id, train_date)
		VALUES(?, ?)''', (user, ts))

	for v in exercises_list:
		sets = json.loads(v[2])
		minVal = sets[index := 0]
		for i in range(1, len(sets)):
			if sets[i] < minVal:
				minVal = sets[i]
				index = i

		if v[1] == 'reps':
			sets[index] += 1
			db.cur.execute(f'UPDATE exercises SET (sets, last) = (?, ?)WHERE id = ?',
				(json.dumps(sets), ts, v[0]))
		else:
			sets[index] += 60
			db.cur.execute(f'UPDATE exercises SET (sets, last) = (?, ?)WHERE id = ?',
				(json.dumps(sets), ts, v[0]))

	db.base.commit()

