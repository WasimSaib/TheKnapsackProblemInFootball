class Player:
    def __init__(self,name, id, overall, value,pos):
        self._name = name
        self._id = id
        self._pos = pos
        self._overall = overall
        self._value = value//1000
        # self._selected = 0 #will be one if selected
    def __repr__(self):
        return f'{self._id}, {self._name}, {self._pos}, {self._overall}'
        