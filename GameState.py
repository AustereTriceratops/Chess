class gameState():
    def __init__(self):
        self.grid = [[cell() for _ in range(8)] for _ in range(8)]
        print(self.grid)


class cell():
    def __init__(self):
        self.id = '0'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.id
