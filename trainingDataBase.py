import dataBase as db
import json
import datetime
import re


def setsProcessing(sets):
	try:
	    sets = re.findall(r'\d+', sets)
	    for i, v in enumerate(sets):
	        sets[i] = int(sets[i])
	    return sets
	except Exception as e:
		print(e)
		return [0]
    
def checkExercise(user_id, name, exeType, weight):
	db.cur.execute('''SELECT name, type, weight FROM exercises WHERE
		user_id = ? AND name = ? AND type = ? AND weight = ?''', (user_id, name, exeType, weight))
	if db.cur.fetchone():
		return True
	else:
		return False

def addTraining(user_id, name, exeType, weight, sets, rest):
	sets = json.dumps(sets)
	db.cur.execute('''INSERT INTO exercises
		(user_id, name, type, weight, sets, rest)
		VALUES(?, ?, ?, ?, ?, ?)''', (user_id, name, exeType, weight, sets, rest))
	db.base.commit()

def getTrainingList(user_id):
	db.cur.execute('''SELECT name, type, weight FROM exercises WHERE user_id = ?''', (user_id,))
	trainings =  db.cur.fetchall()
	for i, v in enumerate(trainings):
		trainings[i] = list(v)
	return trainings

def removeTraining():
	pass