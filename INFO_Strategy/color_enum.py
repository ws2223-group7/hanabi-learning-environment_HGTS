from enum import Enum
class Color(Enum):
    __ordering__ = ['R', 'G','B','Y','W']

    R = 1
    G = 2     
    B = 3
    Y = 4 
    W = 5

if __name__ == "__main__":
    red = Color['R']
    green = Color['G']
    blue = Color['B']
    yellow = Color['Y']
    white = Color['W']
    liste = [white.value, yellow.value, blue.value, red.value, green.value]
    liste.sort()
    listColor = [Color(value).name for value in liste]
    print(listColor)

