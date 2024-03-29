class Exercise:
    def __init__(self, name='Default Exercise', user_id=0):
        self.id = 0
        self.name = name
        self.user_id = user_id
        self.type = 'reps'
        self.weight = 'Свой вес'
        self.sets = [1, 1, 1, 1, 1]
        self.rest = 60
        self.last = 1.0
        self.max_reps = 50
        self.add_reps = 1
        self.add_order = [0, 1, 2, 3, 4]

    def do_reps(self, iter_number=1):
        if self.add_reps == 0:
            return

        for _ in range(iter_number):
            flag = 0
            while flag < len(self.add_order):
                if self.sets[self.add_order[0]] < self.max_reps:
                    if self.sets[self.add_order[0]] + self.add_reps <= self.max_reps:
                        self.sets[self.add_order[0]] += self.add_reps
                        flag = len(self.add_order) + 1
                    else:
                        self.sets[self.add_order[0]] = self.max_reps
                        flag = len(self.add_order) + 1
                else:
                    flag += 1
                self.add_order = self.add_order[1:] + self.add_order[:1]
            else:
                if flag == len(self.add_order):
                    self.add_reps = 0

    def rollback(self):
        if self.sets[self.add_order[-1]] - self.add_reps >= 0:
            self.sets[self.add_order[-1]] -= self.add_reps
        else:
            self.sets[self.add_order[-1]] = 0
        self.add_order = self.add_order[-1:] + self.add_order[:-1]
        self.last = 1.0

    def copy(self):
        newExercise = Exercise(name=self.name, user_id=self.user_id)
        newExercise.id = self.id
        newExercise.type = self.type
        newExercise.weight = self.weight
        newExercise.sets = self.sets.copy()
        newExercise.rest = self.rest
        newExercise.last = self.last
        newExercise.max_reps = self.max_reps
        newExercise.add_reps = self.add_reps
        newExercise.add_order = self.add_order.copy()

        return newExercise

    def __eq__(self, other):
        return (self.name == other.name and self.user_id == other.user_id and
                self.type == other.type and self.weight == other.weight)


class Training:
    def __init__(self, name='Default Training', user_id=0):
        self.id = 0
        self.name = name
        self.user_id = user_id
        self.priority = 'Обычный'
        self.rest = 60
        self.last = 1.0
