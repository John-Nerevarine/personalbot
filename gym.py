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
        for _ in range(iter_number):
            self.sets[self.add_order[0]] += self.add_reps
            self.add_order = self.add_order[1:] + self.add_order[:1]

    def remove_one_train(self):
        self.sets[self.add_order[-1]] -= self.add_reps
        self.add_order = self.add_order[-1:] + self.add_order[:-1]
        self.last = 1.0


class Training:
    def __init__(self, name='Default Training', user_id=0):
        self.id = 0
        self.name = name
        self.user_id = user_id
        self.priority = 'Обычный'
        self.rest = 60
        self.last = 1.0