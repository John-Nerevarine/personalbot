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
        while len(sets) < 5:
            sets.append(0)
        return sets[:5]

    except Exception as e:
        print(e)
        return [0, 0, 0, 0, 0]

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

# можно ли удалять упражнение
def getTrainsWithExercise(user_id, exercise):
    db.cur.execute('''SELECT name FROM trainings_consist JOIN trainings on training_id = trainings.id
        WHERE user_id = ? AND exercise_name = ?''', (user_id, exercise))
    inUseTrainings = db.cur.fetchall()
    if not inUseTrainings:
        return False

    db.cur.execute('''SELECT id FROM exercises WHERE user_id = ? AND name = ?''', (user_id, exercise))
    exercisesIds = db.cur.fetchall()
    if len(exercisesIds) > 1:
        return False

    return inUseTrainings

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
        trainings_consist ON name = exercise_name WHERE training_id = ?
        GROUP BY name HAVING last = MIN(last) ORDER BY trainings_consist.id ASC''', (train_id,))
    return db.cur.fetchall()

def pushDataToSheets(user, exercises):
    db.cur.execute('''SELECT train_date FROM days
        WHERE user_id = ?
        GROUP BY user_id HAVING train_date = MAX(train_date)''', (user,))
    last_train = db.cur.fetchone()
    if not(last_train):
        last_train = 0
    else: last_train = last_train[0]

    ts = time.time()
    currentYear = datetime.datetime.fromtimestamp(ts).year
    currentMonth = datetime.datetime.fromtimestamp(ts).month
    currentDay = datetime.datetime.fromtimestamp(ts).day
    lastYear = datetime.datetime.fromtimestamp(last_train).year
    lastMonth = datetime.datetime.fromtimestamp(last_train).month
    lastDay = datetime.datetime.fromtimestamp(last_train).day

    client = pygsheets.authorize(service_account_file=GS_KEY)
    spreadsht = client.open(SPSHEET)

    workSheetName = f'{currentMonth}.{currentYear}'

    if currentYear != lastYear or currentMonth != lastMonth:
        lastDay = 0
        spreadsht.add_worksheet(workSheetName)
        worksht = spreadsht.worksheet_by_title(workSheetName)
        worksht.index = 0
        worksht.update_values(crange= 'A1:H1', values=[['Число', 'Упражнение', 'I', 'II', 'III', 'IV', 'V', 'Всего']])
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

    if not(currentDay == lastDay or currentDay == lastDay+1):

        valueMatrix = []
        for i in range(lastDay+1, currentDay):
            valueMatrix.append([i, '-'])
    
        modelCell.color = (0.8, 0.8, 0.8, 0)
        modelCell.set_text_format('bold', False)
        modelCell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)
        startIndex = lastRow+1
        endIndex = currentDay-lastDay+lastRow-1
        rng = pygsheets.datarange.DataRange(start='A'+str(startIndex), end='H'+str(endIndex), worksheet=worksht)
        rng.update_values(valueMatrix)
        rng.apply_format(modelCell)
        rng.update_borders(top=True,
                           right=True,
                           bottom=True,
                           left=True,
                           style='SOLID')

    startIndex = currentDay-lastDay+lastRow + (1 if currentDay == lastDay else 0)
    endIndex = startIndex+len(exercises)-1
    rng = pygsheets.datarange.DataRange(start='A'+str(startIndex), end='H'+str(endIndex), worksheet=worksht)

    # id, name, type, weight, sets, rest
    valueMatrix =[]
    for i, v in enumerate(exercises):
        sets = json.loads(v[4])
        if v[2] == 'time':
            name = v[1] + ', вес: ' + v[3] + ', на время'
            for j, k in enumerate(sets):
                sets[j] = int(sets[j]/60*100)/100
        else: name = v[1]

        formula = f'=SUM(C{str(startIndex+i)}:G{str(startIndex+i)})'
        valueMatrix.append(['', name, *sets,  formula])
    valueMatrix[0][0] = currentDay

    rng.update_values(valueMatrix)

    modelCell.color = (1, 1, 1, 0)
    modelCell.set_text_format('bold', False)
    modelCell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)
    modelCell.set_vertical_alignment(pygsheets.custom_types.VerticalAlignment.MIDDLE)
    modelCell.wrap_strategy = 'WRAP'
    rng.apply_format(modelCell)

    rng = pygsheets.datarange.DataRange(start='A'+str(startIndex), end='A'+str(endIndex), worksheet=worksht)
    rng.update_borders(top=True,
                       right=True,
                       bottom=True,
                       left=True,
                       style='SOLID')
    
    rng = pygsheets.datarange.DataRange(start='B'+str(startIndex), end='H'+str(endIndex), worksheet=worksht)
    rng.update_borders(top=True,
                       right=True,
                       bottom=True,
                       left=True,
                       style='SOLID')

    modelCell.color = (1, 0.7, 0.7, 0)
    rng = pygsheets.datarange.DataRange(start='C'+str(startIndex), end='G'+str(endIndex), worksheet=worksht)
    rng.apply_format(modelCell)
    rng.update_borders(top=True,
                       right=True,
                       bottom=True,
                       left=True,
                       inner_vertical=True,
                       inner_horizontal=True,
                       style='SOLID')

def playTraining(train_id, exercises_list, user):
    ts = time.time()
    db.cur.execute(f'UPDATE trainings SET last = ? WHERE id = ?',
        (ts, train_id))

    db.cur.execute('''INSERT INTO days (user_id, train_date)
        VALUES(?, ?)''', (user, ts))


    # id, name, type, weight, sets, rest
    for v in exercises_list:
        sets = json.loads(v[4])
        index = 0
        minVal = sets[index]
        for i in range(1, len(sets)):
            if sets[i] < minVal and sets[i] != 0:
                minVal = sets[i]
                index = i

        if v[2] == 'reps':
            sets[index] += 1
            db.cur.execute(f'UPDATE exercises SET (sets, last) = (?, ?)WHERE id = ?',
                (json.dumps(sets), ts, v[0]))
        else:
            sets[index] += 60
            db.cur.execute(f'UPDATE exercises SET (sets, last) = (?, ?)WHERE id = ?',
                (json.dumps(sets), ts, v[0]))

    db.base.commit()

def getLastTrainingDate(user_id):
    db.cur.execute('''SELECT train_date FROM days 
        WHERE user_id = ?
        GROUP BY user_id HAVING train_date = MAX(train_date)''', (user_id,))
    ret = db.cur.fetchone()
    if ret:
        return ret[0]
    else:
        return 0

def getOldestTraining(user_id, priority = None):
    priorityExist = False

    if priority:
        db.cur.execute('''SELECT priority FROM trainings WHERE user_id = ? AND priority = ?''', (user_id, priority))
        if db.cur.fetchone():
            priorityExist = True

    if priorityExist:
        db.cur.execute('''SELECT exe_id, exe_name, exe_type,
            exe_weight, exe_sets, exe_rest,
            trainings.id, trainings.name, trainings.rest
            FROM
            (SELECT exercises.id as exe_id, name as exe_name, type as exe_type,
            weight as exe_weight, sets as exe_sets, rest as exe_rest, training_id
            FROM exercises JOIN trainings_consist
            ON name = exercise_name
            WHERE training_id = (SELECT id FROM trainings WHERE
            user_id = ? AND priority = ? GROUP BY user_id HAVING MIN(last))
            GROUP BY name HAVING last = MIN(last)
            ORDER BY trainings_consist.id ASC)

            JOIN trainings ON trainings.id = training_id''',
            (user_id, priority))
        training = db.cur.fetchall()
        
    else:
        db.cur.execute('''SELECT exe_id, exe_name, exe_type,
            exe_weight, exe_sets, exe_rest,
            trainings.id, trainings.name, trainings.rest
            FROM
            (SELECT exercises.id as exe_id, name as exe_name, type as exe_type,
            weight as exe_weight, sets as exe_sets, rest as exe_rest, training_id
            FROM exercises JOIN trainings_consist
            ON name = exercise_name
            WHERE training_id = (SELECT id FROM trainings WHERE
            user_id = ? GROUP BY user_id HAVING MIN(last))
            GROUP BY name HAVING last = MIN(last)
            ORDER BY trainings_consist.id ASC)

            JOIN trainings ON trainings.id = training_id''', (user_id,))
        training = db.cur.fetchall()
    return training
