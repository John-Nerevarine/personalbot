# Personal Bot
Чат-бот на Python в Telegram для автоматизации рутинных процессов.(бот в разработке)

## Оглавление
1. [Цель создания](https://github.com/John-Nerevarine/personalbot#1-цель-создания)
2. [Функционал](https://github.com/John-Nerevarine/personalbot#2-функционал)
    1. [Физкультура](https://github.com/John-Nerevarine/personalbot#физкультура)
    2. [Автомобиль](https://github.com/John-Nerevarine/personalbot#автомобиль)
3. [Реализация](https://github.com/John-Nerevarine/personalbot#3-реализация)
    1. [Список модулей](https://github.com/John-Nerevarine/personalbot#список-модулей)
    2. [Скриншоты](https://github.com/John-Nerevarine/personalbot#скриншоты)
    3. [Описание модулей](https://github.com/John-Nerevarine/personalbot#описание-модулей)


## 1. Цель создания.
В повседневной жизни имею склонность собирать и систематизировать информацию о своей жизнедеятельности. В этом плане мне очень помогают Google таблицы - простота и гибкость позволяют использовать их практичести под любые задачи. Со временем у меня собралось довольно много таблиц - доходы, расходы, инвестиции, владение автомобилем, физкультура и пр. И долгое время меня всё устраивало, но со временем стало очевидно, что ввод данных в каждую таблицу может быть автоматизирован. Для этого и был создан данный чат бот.
Бот был создан исключительно для личного использования, но тем не менее проектировался как допускающий в будущем возможность доработки под нескольких пользователей. В данный момент доступ к боту есть только у меня.
> *[Оглавление](https://github.com/John-Nerevarine/personalbot#оглавление)*

## 2. Функционал.
### Физкультура.
Не вызывает сомнений тот факт, что физическая активность абсолютно необходима для здоровья человека. Не так важно, посещается зал, спортивная площадка во дворе или тренировки проводятся в домашних условиях - организму в целом без разницы сколько стоит и как выглядит спорт инвентарь. Главное соблюдать сбалансированность, систематичность и технику выполнения упражнений.
Мой выбор был сделан в пользу домашних тренировок с периодическим воркаутом на улице.
Итак, я вёл Гугл таблицу, где вводил сколько подходов какого упражнения в какой день я сделал, чтобы можно видеть прогресс и планировать следующие тренировки. Это было удобно, но перед каждой тренировкой просмотр предыдущих дней, выбор упражнений, подбор весов и ввод всего этого в таблицу требовало до 10 минут, что иногда было критично, когда тренировка проходила в условиях ограниченного времени. Решено было возложить все рутинные функции на бота.
Фукционал предусматривает сохранение упражнений, повторов и подходов, группировка упражнений в тренировки, возможность редактирования тренировок и упражнений, возможность выбора конкретной тренировки и самое главное - возможность автоматического выбора тренировки. 
Забегая вперёд, теперь на выбор тренировки уходит не более 10 секунд, так что цель достигнута.
> *[Оглавление](https://github.com/John-Nerevarine/personalbot#оглавление)*

### Автомобиль.
Данный пункт находится в разработке. Запланированно добавление в Google таблицу данных о затратах на автомобиль и вывод аналитических данных: расход на 100км, стоимость владения и пр.
> *[Оглавление](https://github.com/John-Nerevarine/personalbot#оглавление)*

## 3. Реализация.
Для взаимодействия с Telegram Bot API в боте использована библиотека aiogram. Для хранения данных используется SQLite и библиотека sqlite3.
Была попытка сделать "приложение" на базе Telegram. то есть пользователь видит только одно сообщение, которое редактируется в процессе взаимодействия, а сообщения же самого пользователя удаляются. В целом, реализация удалась, но иногда Telegram показывает уже удалённые сообщения. Вероятно какой-то баг API.

> Следует сделать замечание, что здесь и далее слово "training" я использовал в значении "тренировка", что с точки зрения английского языка не правильно. Однако, переведчиком я догадался воспользоваться только тогда, когда бот уже использовался по назначению. Я и решил всё не переделывать, так как на функционал это не влияет.

Бот состоит из 16 модулей. Каждый модуль отвечает за определённый функционал бота.

### Список модулей:
- **[bot.py](https://github.com/John-Nerevarine/personalbot#botpy)**
- **[createBot.py](https://github.com/John-Nerevarine/personalbot#createbotpy)**
- **[config.py](https://github.com/John-Nerevarine/personalbot#configpy)** *(не представлен в репозитории)*
- **[dataBase.py](https://github.com/John-Nerevarine/personalbot#databasepy)**
- **[keyboards.py](https://github.com/John-Nerevarine/personalbot#keyboardspy)**
- **[support.py](https://github.com/John-Nerevarine/personalbot#supportpy)**
- **[trainingsMenu.py](https://github.com/John-Nerevarine/personalbot#trainingsmenupy)**
- **[mainMenu.py](https://github.com/John-Nerevarine/personalbot#mainmenupy)**
- **trainingsActions**
    - **[__init__.py](https://github.com/John-Nerevarine/personalbot#trainingsactionsinitpy)**
    - **[addExercise.py](https://github.com/John-Nerevarine/personalbot#trainingsactionsaddexercisepy)**
    - **[addTraining.py](https://github.com/John-Nerevarine/personalbot#trainingsactionsaddtrainingpy)**
    - **[editExercise.py](https://github.com/John-Nerevarine/personalbot#trainingsactionseditexercisepy)**
    - **[editTraining.py](https://github.com/John-Nerevarine/personalbot#trainingsactionsedittrainingpy)**
    - **[trainingChoise.py](https://github.com/John-Nerevarine/personalbot#trainingsactionstrainingchoicepy)**
    - **[trainingDataBase.py](https://github.com/John-Nerevarine/personalbot#trainingsactionstrainingdatabasepy)**
    - **[trainingQuick.py](https://github.com/John-Nerevarine/personalbot#trainingsactionstrainingquickpy)**

> *[Оглавление](https://github.com/John-Nerevarine/personalbot#оглавление)*

### Скриншоты
(будут добавлены в будущем)
> *[Оглавление](https://github.com/John-Nerevarine/personalbot#оглавление)*

### Описание модулей
### [bot.py](https://github.com/John-Nerevarine/personalbot/blob/main/bot.py)
Основной модуль бота. Служит центральным связующим звеном между остальными модулями, а также запускает бота.
Первой строкой указыватся путь к Python в виртуальном окружении. Затем импортируются необходимые модули бота, executor из aiogram.utils, диспетчер из модуля createBot.
В модуле есть только одна функция on_startup(), которая выполняется при запуске. Она запускает фукнцию sqlStart() модуля dataBase, для подключения к базе данных.
После объявления функций регистрируются обработчики из импортированных модулей.
Ну и в последнюю очередь запускается поллинг, который и вызывает функцию on_startup().


### [createBot.py](https://github.com/John-Nerevarine/personalbot/blob/main/createBot.py)
Создание бота, определения "общих" переменных и состояний.
Производится импорт основных элементов бота из библиотеки aiogram и токена бота из модуля config. Затем объявляются MemoryStorage, непосредственно сам объект Бота, диспетчер, глобальные текстовые переменные и подклассы состояния. Все события в игре привязаны к состояниям. Определённые действия могут быть совершены только в опредёленном состоянии. И соответственно, действия изменяют текущее состояние.


### config.py
Данный модуль не представлен в репозитории. Он содержит в себе токен бота, ключ API Google Sheets, id Telegram аккаунта администратора и название Google таблицы. Сделано отдельным модулем для простоты загрузки на сервер в случае смены каких-либо значений.


### [dataBase.py](https://github.com/John-Nerevarine/personalbot/blob/main/dataBase.py)
Создание базы данных. Все запросы к базе вынесены в отдельные модули в соответствии с назначением: *trainingsActions/trainingsDataBase.py*
Для Физкультуры создаётся четыре таблицы.

- trainings - cодержит в себе информацию о существующих тренировках.

| Значение | Описание |
|----:|:----|
| id | id тренировки. Целое число. |
| name | Название тренировки. Строка. |
| user_id | id пользователя создавшего, тренировку. Целое число. |
| priority | Приоритет тренировки. Строка. Может иметь значения: "Высокий", "Обычный", "Особый". |
| rest | Время отдыха между упражениями. Целое число. |
| last | Временная метка последнего использования тренировки. Дробное число. По умолчанию "1.0" |



- exercises - cодержит в себе информацию о существующих упражнениях.

| Значение | Описание |
|----:|:----|
| id | id упражнения. Целое число. |
| name | Название упражнения. Строка. |
| user_id | id пользователя, создавшего упражнение. Целое число. |
| type | Тип упражнения. Строка. Может иметь значения: "time", "reps. |
| weight | Вес, с которым выполняется упражнение. Строка. |
| sets | Количество повторов по подходам. Строка. Хранится json. |
| rest | Время отдыха между подходами. Целое число. |
| last | Временная метка последнего использования тренировки. Дробное число. По умолчанию "1.0" |



- trainings_consist - cодержит в себе информацию об упражнениях содержащихся в конкретных тренировках.

| Значение | Описание |
|----:|:----|
| id | id записи. Целое число. Использутся для сортировки упражнения в тренировке. |
| training_id | id тренировки. Целое число. Использутся для связи с таблицей "trainings". |
| exercise_name | Название упражнения. Строка. Использутся для связи с таблицей "exercises". |



- days - cодержит в себе информацию об том, когда была последняя тренировка пользователя.

| Значение | Описание |
|----:|:----|
| id | id записи. Целое число. |
| user_id | id пользователя. Целое число. |
| train_date | Дата тренировки. |


### [keyboards.py](https://github.com/John-Nerevarine/personalbot/blob/main/keyboards.py)
Объявление кнопок, возвращаемых значений этих кнопок, и клавиатур. Часть клавиатур фомируются непосредственно в процессе работы бота и здесь не описаны.


### [mainMenu.py](https://github.com/John-Nerevarine/personalbot/blob/main/mainMenu.py)
Начало работы с ботом.

| Функция | Описание |
|----:|:----|
|[commandStart(message: types.Message, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/mainMenu.py#L10)|Запуск главного меню командой "/start". Проверка пользователя: если одобрен - показ основного меню, если нет - запись id пользователя в лог, показ сообщения о невозможности продолжить.|
|[callbackMainMenu(callback_query: types.CallbackQuery,state: FSMContex)](https://github.com/John-Nerevarine/personalbot/blob/main/mainMenu.py#L32)|Возврат в главное меню по кнопке. Сброс состояний, хранилища - начало работы программы с нуля.|
|[getBackData(state:  FSMContext, message)](https://github.com/John-Nerevarine/personalbot/blob/main/mainMenu.py#L47)|Сохранение в список текущего состояния, сообщения и клавиатуры. Запускается почти каждый раз при переходе в следующее меню.|
|[callbackGoBack(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/mainMenu.py#L54)|Возврат на одно меню назад. Загрузка состояния, клавиатуры и сообщения из памяти. Если на момент вызова состояние не определено, вызывается функция [callbackEmergencyStart](https://github.com/John-Nerevarine/personalbot/blob/main/support.py#L8) модуля [support.py](https://github.com/John-Nerevarine/personalbot/blob/main/support.py).|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/mainMenu.py#L77)|Регистрация обработчиков событий.|


### [support.py](https://github.com/John-Nerevarine/personalbot/blob/main/support.py)
Дополнительные служебные функции.

| Функция | Описание |
|----:|:----|
|[callbackEmergencyStart(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/support.py#L8)|Перезапуск главного меню. Вызывается, если на кнопку нет обработчика. Таким образом предотвращается ситуация, в которой бот перестаёт отвечать на нажатие кнопок.|
|[commandDeleteMessage(message: types.Message, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/support.py#L31)|Удаление введённого пользователем сообщения. Вызывается при любом вводе пользователя после его обработки, если ввод уместен.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/support.py#L34)|Регистрация обработчиков событий.|


### [trainingsMenu.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsMenu.py)
Вывод меню Физкультуры.

| Функция | Описание |
|----:|:----|
|[callbackTrainingsMain(callback_query:types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsMenu.py#L11)|Вывод меню Физкультуры.|
|[callbackTrainingsSettings(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsMenu.py#L21)|Меню настроек Физкультуры.|
|[callbackShowExercisesList(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsMenu.py#L30)|Вывод списка упражнений.|
|[callbackShowTrainingsList(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsMenu.py#L69)|Вывод списка тренировок.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsMenu.py#L107)|Регистрация обработчиков событий.|


### [trainingsActions/__init__.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/__init__.py)
Регистрация модулей каталога в программе.


### [trainingsActions/addExercise.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addExercise.py)
Добавление упражнений.

| Функция | Описание |
|----:|:----|
|[callbackAddExercise(callback_query: types.CallbackQuery, state: FSMContext](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addExercise.py#L10)|Начало добавления упражнения, запрос названия к пользователю.|
|[commandsAddExercise(message: types.Message, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addExercise.py#L22)|Обработка ввода пользователя в зависимости от этапа добавления.|
|[callbackAddExerciseType(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addExercise.py#L108)|Запрос у пользователя, какой снаряд какого веса используется в упражнении.|
|[callbackAddExerciseConfirm(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addExercise.py#L122)|Добавление упражнения в базу данных.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addExercise.py#L153)|Регистрация обработчиков событий.|


### [trainingsActions/addTraining.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addTraining.py)
Добавление тренировок.

| Функция | Описание |
|----:|:----|
|[callbackAddTraining(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addTraining.py#L10)|Начало добавления тренировки. Запрос к пользователю названия тренировки.|
|[commandsAddTraining(message: types.Message, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addTraining.py#L22)|Обработка ввода пользователя в зависимости от этапа добавления.|
|[callbackAddTrainingPriority(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addTraining.py#L54)|Запрос времени отдыха между упражнениями.|
|[callbackAddTrainingConfirm(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addTraining.py#L68)|Добавление тренировки в базу данных.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/addTraining.py#L97)|Регистрация обработчиков событий.|


### [trainingsActions/editExercise.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py)
Редактирование упражнений.

| Функция | Описание |
|----:|:----|
|[callbackShowExercises(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L11)|Вывод меню из существующих упражнений.|
|[callbackEditExerciseName(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L35)|Вывод меню из возможных типов выбранного упражнения.|
|[callbackEditExerciseType(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L60)|Вывод меню из возможных весов выбранного упражнения.|
|[callbackEditExerciseWeight(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L85)|Вывод меню из возможных действий для выбранного упражнения.|
|[callbackEditExerciseRemove(callback_query: types.CallbackQuery, state: FSMContext](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L109)|Удаление выбранного упражнения.|
|[callbackEditExercise(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L163)|Вывод подробностей об упражнении и меню из параметров для редактирования.|
|[callbackEditExerciseNewName(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L199)|Запрос к пользователю ввести новое название для упражнения.|
|[callbackEditExerciseNewType(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L212)|Запрос к пользователю выбрать новый тип для упражнения.|
|[callbackEditExerciseNewWeight(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L225)|Запрос к пользователю ввести новый вес для упражнения.|
|[callbackEditExerciseNewSets(callback_query: types.CallbackQuery, state: FSMContext](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L238)|Запрос к пользователю ввести новое количество повторов для упражнения.|
|[callbackEditExerciseNewRest(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L251)|Запрос к пользователю ввести новое время отдыха между повторами для упражнения.|
|[showEditedExerciseMessage(user_id, keyboard, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L264)|Вывод меню редактирования с изменённым упражнением.|
|[callbackEditExerciseNewTypeSet(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L278)|Проверка упражнения на уникальность после выбора типа.|
|[commandsEditExercise(message: types.Message, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L316)|Обработка ввода от пользователя в зависимости от редактируемого параметра.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editExercise.py#L398)|Регистрация обработчиков событий.|


### [trainingsActions/editTraining.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py)
Редактирование тренировок.

| Функция | Описание |
|----:|:----|
|[callbackShowTrainingsForEdit(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L11)|Вывод меню из существующих тренировок.|
|[callbackEditTraining(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L30)|Вывод доступных действий для выбранной тренировки.|
|[callbackEditTrainingName(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L71)|Ввод нового названия тренировки.|
|[callbackEditTrainingPriority(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L84)|Выбор приоритета тренировки.|
|[callbackEditTrainingPrioritySet(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L99)|Измениние приоритета тренировки на выбранный.|
|[callbackEditTrainingRest(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L115)|Ввод нового времени отдыха между упражнениями.|
|[callbackEditTrainingAddExe(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L128)|Вывод меню из существующих упражнений для добавления в тренировку.|
|[callbackEditTrainingAddExeChoice(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L161)|Добавление упражнения в тренировку.|
|[callbackEditTrainingRemoveExe(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L186)|Вывод меню из упражнений в тренировке для удаления.|
|[callbackEditTrainingRemoveExeChoice(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L215)|Удаление выбранного упражнения из тренировки.|
|[callbackEditTrainingRemoveTrain(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L239)|Удаление выбранной тренировки.|
|[showEditedTrainingMessage(user_id, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L254)|Вывод меню редактирования с изменённой тренировкой.|
|[commandsEditTraining(message: types.Message, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L287)|Обработка ввода пользователя при редактировании тренировки.|
|[callbackShowLastTrainingDate(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L324)|Показать дату последней тренировки. Данная функция используется для удаления информации о последней проведённой тренировке.|
|[callbackRemoveLastTrainingDate(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L344)|Удаление даты последней тренировки.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/editTraining.py#L354)|Регистрация обработчиков событий.|


### [trainingsActions/trainingChoice.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingChoice.py)
Выбор тренировки.

| Функция | Описание |
|----:|:----|
|[callbackShowTrainingsForPlay(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingChoice.py#L10)|Показать меню из существующих тренировок.|
|[callbackChoiceTrainingsForPlay(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingChoice.py#L33)|Показать детали выбранной тренировки.|
|[allbackConfirmTrainingsForPlay(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingChoice.py#L63)|Добавление тренировки в Google таблицу и внесение необходимых изменений в базу данных.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingChoice.py#L84)|Регистрация обработчиков событий.|


### [trainingsActions/trainingDataBase.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py)
Запросы к базе данных физкультуры.

| Функция | Описание |
|----:|:----|
|[setsProcessing(sets)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L9)|Обработка ввода количества повторов. Возврат списка из пяти целых чисел.|
|[checkExercise(user_id, name, exeType, weight)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L23)|Проверка в базе данных, что упражнение уже существует. Возврат логическое значение.|
|[addExercise(user_id, name, exeType, weight, sets, rest)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L32)|Добавление нового упражнения в базу данных.|
|[getExerciseList(user_id)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L40)|Получение списка упражнений пользователя. Возвращает двумерный список или False, если упражнений нет.|
|[getTrainsWithExercise(user_id, exercise)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L51)|Проверяет наличие упражнения в каких-либо тренировках. Возвращает False или список тренировок, в которых задействовано упражнение.|
|[removeExercise(user_id, name, exeType, weight)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L66)|Удаление упражнения из базы.|
|[editExercise(exeId, param, new)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L73)|Изменение одного параметра упражнения.|
|[getTrainingsList(user_id)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L79)|Получение списка тренировок пользователя. Возвращает двумерный список или False, если тренировок нет.|
|[isTrainingExist(user_id, name)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L90)|Проверяет существование тренировки. Возвращает логическое значение.|
|[addTraining(user_id, name, priority, rest)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L99)|Добавление тренировки в базу.|
|[getExercisesInTrain(train_id)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L106)|Получить список упражнений в тренировке.|
|[editTraining(trainId, param, new)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L116)|Изменить один параметр тренировки|
|[addExerciseInTrain(train, exe)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L122)|Добавить упражение в тренировку.|
|[removeExerciseFromTrain(train_id, exe)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L129)|Удалить упражнение из тренировки.|
|[removeTraining(train_id)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L136)|Удалить тренировку.|
|[getActualTrainingExerciseList(train_id)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L146)|Получить список упражнений в тренировке в зависимости от того, с каким весом упражнение делалось до этого.|
|[pushDataToSheets(user, exercises)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L153)|Добавление тренировки в Google таблицу.|
|[playTraining(train_id, exercises_list, user)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L275)|Изменения базы данных в связи с использованием тренировки - изменения дат выполнения тренировки и упражнений, изменение количества повторов в упражнении.|
|[getLastTrainingDate(user_id)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L305)|Получить дату последей тренировки.|
|[removeLastTrainingDate(user_id)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L316)|Удаление даты последней тренировки.|
|[getOldestTraining(user_id, priority = None)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py#L323)|Получить тренировку, которая не использовалась наиболее долгое время.|


### [trainingsActions/trainingQuick.py](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingDataBase.py)
Быстрый выбор тренировки. Бот сам выбирает тренировку в зависимости от времени последнего использования.

| Функция | Описание |
|----:|:----|
|[callbackShowQuickTraining(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingQuick.py#L11)|Вывод информации о рекомендуемой тренировке.|
|[callbackConfirmQuickTraining(callback_query: types.CallbackQuery, state: FSMContext)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingQuick.py#L49)|Использование тренировки.|
|[registerHandlers(dp : Dispatcher)](https://github.com/John-Nerevarine/personalbot/blob/main/trainingsActions/trainingQuick.py#L72)|Регистрация обработчиков событий.|


> *[Оглавление](https://github.com/John-Nerevarine/personalbot#оглавление)*
