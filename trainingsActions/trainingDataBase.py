import datetime
import json
import re
import time

import pygsheets

import dataBase as db
import gym
from config import GS_KEY, SPSHEET


# Processing input of sets
def setsProcessing(sets):
    try:
        sets = re.findall(r'\d+', sets)
        for i, v in enumerate(sets):
            sets[i] = int(sets[i])
        while len(sets) < 5:
            sets.append(0)
        return sets[:5]

    except Exception as e:
        print(e)
        return [0, 0, 0, 0, 0]


# Check exercise existence
def checkExercise(exe):
    db.cur.execute('''SELECT name, type, weight FROM exercises WHERE
        user_id = ? AND name = ? AND type = ? AND weight = ?''', (exe.user_id, exe.name, exe.type, exe.weight))
    if db.cur.fetchone():
        return True
    else:
        return False


# Add exercise
def addExercise(exe):
    if exe.type == 'reps':
        db.cur.execute('''INSERT INTO exercises
            (user_id, name, type, weight, sets, rest)
            VALUES(?, ?, ?, ?, ?, ?)''', (exe.user_id, exe.name, exe.type, exe.weight,
                                          json.dumps(exe.sets), exe.rest))
    else:
        db.cur.execute('''INSERT INTO exercises
            (user_id, name, type, weight, sets, rest, add_reps, max_reps, add_order)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (exe.user_id, exe.name, exe.type, exe.weight,
                        json.dumps(exe.sets), exe.rest, exe.add_reps, exe.max_reps, "[0, 0, 0, 0, 0]"))
    db.base.commit()


# Get list of exercises

def getExerciseList(user_id):
    db.cur.execute('''SELECT * FROM exercises WHERE user_id = ?''', (user_id,))
    exercises_raw = db.cur.fetchall()
    if exercises_raw:
        exercises = []
        for exe in exercises_raw:
            exercises.append(gym.Exercise(name=exe[1]))
            exercises[-1].id = exe[0]
            exercises[-1].user_id = exe[2]
            exercises[-1].type = exe[3]
            exercises[-1].weight = exe[4]
            exercises[-1].sets = json.loads(exe[5])
            exercises[-1].rest = exe[6]
            exercises[-1].last = exe[7]
            exercises[-1].max_reps = exe[8]
            exercises[-1].add_reps = exe[9]
            exercises[-1].add_order = json.loads(exe[10])
        return exercises
    else:
        return False


# Check ability to remove exercise
def getTrainsWithExercise(exe):
    db.cur.execute('''SELECT name FROM trainings_consist JOIN trainings on training_id = trainings.id
        WHERE user_id = ? AND exercise_name = ?''', (exe.user_id, exe.name))
    inUseTrainings = db.cur.fetchall()
    if not inUseTrainings:
        return False

    db.cur.execute('''SELECT id FROM exercises WHERE user_id = ? AND name = ?''', (exe.user_id, exe.name))
    exercisesIds = db.cur.fetchall()
    if len(exercisesIds) > 1:
        return False

    return inUseTrainings


# Remove exercise
def removeExercise(exe):
    db.cur.execute('''DELETE FROM exercises
        WHERE user_id = ? AND name = ? AND type = ? AND weight = ?''',
                   (exe.user_id, exe.name, exe.type, exe.weight))
    db.base.commit()


# Change one parameter of exercise
def editExercise(exeId, param, new):
    db.cur.execute(f'UPDATE exercises SET {param} = ? WHERE id = ?',
                   (new, exeId))
    db.base.commit()


# Get list of trainings
def getTrainingsList(user_id):
    db.cur.execute('''SELECT * FROM trainings WHERE user_id = ?''', (user_id,))
    trainings_raw = db.cur.fetchall()
    if trainings_raw:
        trainings = []
        for train in trainings_raw:
            trainings.append(gym.Training(name=train[1]))
            trainings[-1].id = train[0]
            trainings[-1].user_id = train[2]
            trainings[-1].priority = train[3]
            trainings[-1].rest = train[4]
            trainings[-1].last = train[5]
        return trainings
    else:
        return False


def isTrainingExist(train):
    db.cur.execute('''SELECT name FROM trainings WHERE
        user_id = ? AND name = ?''', (train.user_id, train.name))
    if db.cur.fetchone():
        return True
    else:
        return False


# Add training
def addTraining(train):
    db.cur.execute('''INSERT INTO trainings
        (user_id, name, priority, rest)
        VALUES(?, ?, ?, ?)''', (train.user_id, train.name, train.priority, train.rest))
    db.base.commit()


# Get list of exercises in training
def getExercisesInTrain(train_id):
    db.cur.execute('''SELECT exercise_name FROM trainings_consist WHERE
        training_id = ?''', (train_id,))
    select = db.cur.fetchall()
    ret = []
    for v in select:
        ret.append(v[0])
    return ret


# Change one parameter of training
def editTraining(trainId, param, new):
    db.cur.execute(f'UPDATE trainings SET {param} = ? WHERE id = ?',
                   (new, trainId))
    db.base.commit()


# Add exercise in training
def addExerciseInTrain(train, exe):
    db.cur.execute('''INSERT INTO trainings_consist
        (training_id, exercise_name)
        VALUES(?, ?)''', (train, exe))
    db.base.commit()


# Remove exercise from training
def removeExerciseFromTrain(train_id, exe):
    db.cur.execute('''DELETE FROM trainings_consist
        WHERE training_id = ? AND exercise_name = ?''',
                   (train_id, exe))
    db.base.commit()


# Remove training
def removeTraining(train_id):
    db.cur.execute('''DELETE FROM trainings_consist
        WHERE training_id = ?''',
                   (train_id,))
    db.cur.execute('''DELETE FROM trainings
        WHERE id = ?''',
                   (train_id,))
    db.base.commit()


# Get list of exercises in trainings depending on last date
def getActualTrainingExerciseList(train_id):
    db.cur.execute('''SELECT exercises.id, name, user_id, type, weight, sets, rest,
        last, max_reps, add_reps, add_order
        FROM exercises JOIN
        trainings_consist ON name = exercise_name WHERE training_id = ?
        GROUP BY name HAVING last = MIN(last) ORDER BY trainings_consist.id ASC''', (train_id,))

    exercises_raw = db.cur.fetchall()
    if exercises_raw:
        exercises = []
        for exe in exercises_raw:
            exercises.append(gym.Exercise(name=exe[1]))
            exercises[-1].id = exe[0]
            exercises[-1].user_id = exe[2]
            exercises[-1].type = exe[3]
            exercises[-1].weight = exe[4]
            exercises[-1].sets = json.loads(exe[5])
            exercises[-1].rest = exe[6]
            exercises[-1].last = exe[7]
            exercises[-1].max_reps = exe[8]
            exercises[-1].add_reps = exe[9]
            exercises[-1].add_order = json.loads(exe[10])
        return exercises
    else:
        return False


# Insert trainings data to Google Sheets
def pushDataToSheets(user, exercises):
    # get date of last train
    db.cur.execute('''SELECT train_date FROM days
        WHERE user_id = ?
        GROUP BY user_id HAVING train_date = MAX(train_date)''', (user,))
    last_train = db.cur.fetchone()
    if not last_train:
        last_train = 0
    else:
        last_train = last_train[0]

    ts = time.time()
    currentYear = datetime.datetime.fromtimestamp(ts).year
    currentMonth = datetime.datetime.fromtimestamp(ts).month
    currentDay = datetime.datetime.fromtimestamp(ts).day
    lastYear = datetime.datetime.fromtimestamp(last_train).year
    lastMonth = datetime.datetime.fromtimestamp(last_train).month
    lastDay = datetime.datetime.fromtimestamp(last_train).day

    # connect to googlesheets API
    client = pygsheets.authorize(service_account_file=GS_KEY)
    spreadsht = client.open(SPSHEET)

    workSheetName = f'{currentMonth}.{currentYear}'

    # prepare table
    if currentYear != lastYear or currentMonth != lastMonth:
        lastDay = 0
        spreadsht.add_worksheet(workSheetName)
        worksht = spreadsht.worksheet_by_title(workSheetName)
        worksht.index = 0
        worksht.update_values(crange='A1:H1', values=[['Число', 'Упражнение', 'I', 'II', 'III', 'IV', 'V', 'Всего']])
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
        modelCell = pygsheets.Cell("A1")

    cols = worksht.get_col(2, include_tailing_empty=False)
    lastRow = len(cols)

    if not (currentDay == lastDay or currentDay == lastDay + 1):

        valueMatrix = []
        for i in range(lastDay + 1, currentDay):
            valueMatrix.append([i, '-'])

        modelCell.color = (0.8, 0.8, 0.8, 0)
        modelCell.set_text_format('bold', False)
        modelCell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)
        startIndex = lastRow + 1
        endIndex = currentDay - lastDay + lastRow - 1
        rng = pygsheets.datarange.DataRange(start='A' + str(startIndex), end='H' + str(endIndex), worksheet=worksht)
        rng.update_values(valueMatrix)
        rng.apply_format(modelCell)
        rng.update_borders(top=True,
                           right=True,
                           bottom=True,
                           left=True,
                           style='SOLID')

    startIndex = currentDay - lastDay + lastRow + (1 if currentDay == lastDay else 0)
    endIndex = startIndex + len(exercises) - 1
    rng = pygsheets.datarange.DataRange(start='A' + str(startIndex), end='H' + str(endIndex), worksheet=worksht)

    # prepare data to add to table
    valueMatrix = []
    for i, exe in enumerate(exercises):
        sets = exe.sets.copy()
        if exe.type == 'time':
            name = exe.name + ', вес: ' + exe.weight + ', на время'
            for j, _ in enumerate(sets):
                sets[j] = int(sets[j] / 60 * 100) / 100
        else:
            name = exe.name + ', вес: ' + exe.weight

        formula = f'=SUM(C{str(startIndex + i)}:G{str(startIndex + i)})'
        valueMatrix.append(['', name, *sets, formula])
    valueMatrix[0][0] = currentDay

    # add data to table
    rng.update_values(valueMatrix)

    # format table
    modelCell.color = (1, 1, 1, 0)
    modelCell.set_text_format('bold', False)
    modelCell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)
    modelCell.set_vertical_alignment(pygsheets.custom_types.VerticalAlignment.MIDDLE)
    modelCell.wrap_strategy = 'WRAP'
    rng.apply_format(modelCell)

    rng = pygsheets.datarange.DataRange(start='A' + str(startIndex), end='A' + str(endIndex), worksheet=worksht)
    rng.update_borders(top=True,
                       right=True,
                       bottom=True,
                       left=True,
                       style='SOLID')

    rng = pygsheets.datarange.DataRange(start='B' + str(startIndex), end='H' + str(endIndex), worksheet=worksht)
    rng.update_borders(top=True,
                       right=True,
                       bottom=True,
                       left=True,
                       style='SOLID')

    modelCell.color = (1, 0.7, 0.7, 0)
    rng = pygsheets.datarange.DataRange(start='C' + str(startIndex), end='G' + str(endIndex), worksheet=worksht)
    rng.apply_format(modelCell)
    rng.update_borders(top=True,
                       right=True,
                       bottom=True,
                       left=True,
                       inner_vertical=True,
                       inner_horizontal=True,
                       style='SOLID')


# Changes in the database when trainings has been chosen
def playTraining(train_id, exercises_list, user):
    ts = time.time()
    db.cur.execute(f'UPDATE trainings SET last = ? WHERE id = ?',
                   (ts, train_id))

    db.cur.execute('''INSERT INTO days (user_id, train_date)
        VALUES(?, ?)''', (user, ts))

    for exe in exercises_list:
        exe.do_reps()
        exe.last = ts
        updateExerciseDynamic(exe)


# Update exercise dynamic parameters
def updateExerciseDynamic(exe):
    db.cur.execute(f'UPDATE exercises SET (sets, last, add_order) = (?, ?, ?) WHERE id = ?',
                   (json.dumps(exe.sets), exe.last, json.dumps(exe.add_order), exe.id))
    db.base.commit()


# Get timestamp of last training
def getLastTrainingDate(user_id):
    db.cur.execute('''SELECT train_date FROM days 
        WHERE user_id = ?
        GROUP BY user_id HAVING train_date = MAX(train_date)''', (user_id,))
    ret = db.cur.fetchone()
    if ret:
        return ret[0]
    else:
        return 0


# Remove date of last training in "days"
def removeLastTraining(user_id):
    db.cur.execute('''DELETE FROM days
        WHERE user_id = ? AND train_date = (SELECT MAX(train_date) FROM days WHERE user_id = ?)''',
                   (user_id, user_id))
    db.base.commit()


# Get oldes trainings depending on priority
def getOldestTraining(user_id, priority=None):
    priorityExist = False

    if priority:
        db.cur.execute('''SELECT priority FROM trainings WHERE user_id = ? AND priority = ?''', (user_id, priority))
        if db.cur.fetchone():
            priorityExist = True

    if priorityExist:
        db.cur.execute('''SELECT exe_id, exe_name, exe_type,
            exe_weight, exe_sets, exe_rest, max_reps, add_reps, add_order,
            trainings.id, trainings.name, trainings.rest
            FROM
            (SELECT exercises.id as exe_id, name as exe_name, type as exe_type,
            weight as exe_weight, sets as exe_sets, rest as exe_rest, training_id, max_reps, add_reps, add_order
            FROM exercises JOIN trainings_consist
            ON name = exercise_name
            WHERE training_id = (SELECT id FROM trainings WHERE
            user_id = ? AND priority = ? GROUP BY user_id HAVING MIN(last))
            GROUP BY name HAVING last = MIN(last)
            ORDER BY trainings_consist.id ASC)

            JOIN trainings ON trainings.id = training_id''',
                       (user_id, priority))
    else:
        db.cur.execute('''SELECT exe_id, exe_name, exe_type,
            exe_weight, exe_sets, exe_rest, max_reps, add_reps, add_order,
            trainings.id, trainings.name, trainings.rest
            FROM
            (SELECT exercises.id as exe_id, name as exe_name, type as exe_type,
            weight as exe_weight, sets as exe_sets, rest as exe_rest, training_id, max_reps, add_reps, add_order
            FROM exercises JOIN trainings_consist
            ON name = exercise_name
            WHERE training_id = (SELECT id FROM trainings WHERE
            user_id = ? AND priority != ? GROUP BY user_id HAVING MIN(last))
            GROUP BY name HAVING last = MIN(last)
            ORDER BY trainings_consist.id ASC)

            JOIN trainings ON trainings.id = training_id''', (user_id, 'Особый'))

    training_raw = db.cur.fetchall()
    training = gym.Training(name=training_raw[0][10], user_id=user_id)
    training.id = training_raw[0][9]
    training.rest = training_raw[0][11]
    exercises = []
    for exe in training_raw:
        exercises.append(gym.Exercise(name=exe[1], user_id=user_id))
        exercises[-1].id = exe[0]
        exercises[-1].type = exe[2]
        exercises[-1].weight = exe[3]
        exercises[-1].sets = json.loads(exe[4])
        exercises[-1].rest = exe[5]
        exercises[-1].max_reps = exe[6]
        exercises[-1].add_reps = exe[7]
        exercises[-1].add_order = json.loads(exe[8])

    return training, exercises
