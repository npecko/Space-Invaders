class GameObject:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player(GameObject):
    x_change = 0

    def __init__(self, x, y):
        super().__init__(x, y)

class Enemy(GameObject):
    x_change = 0
    y_change = 0

    def __init__(self, x, y, x_change, y_change):
        super().__init__(x, y)
        self.x_change = x_change
        self.y_change = y_change

class Rocket(GameObject):
    y_change = 0
    rocket_state = ''

    def __init__(self, x, y, y_change, rocket_state):
        super().__init__(x, y)
        self.y_change = y_change
        self.rocket_state = rocket_state

class Life(GameObject):
    pass