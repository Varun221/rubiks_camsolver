from rubik_solver import utils
import time


def verify_cube_string_is_valid(cube_string):
    count = {"G": 0, "B": 0, "R": 0, "Y": 0, "W": 0, "O": 0}

    for c in cube_string:
        count[c] += 1

    for k in count:
        if count[k] != 9:
            print("Uploaded values are wrong!! Terminating the program!")
            time.sleep(2)
            return False

    return True


def generate_cube_string(faces):
    cube_string = ''

    face = faces['up']
    for i in range(3):
        for j in range(3):
            cube_string += face[i][j][0].capitalize()

    order = ['left', 'front', 'right', 'back']
    for o in order:
        face = faces[o]
        for i in range(3):
                for j in range(3):
                    cube_string += face[i][j][0].capitalize()

    face = faces['down']
    for i in range(3):
        for j in range(3):
            cube_string += face[i][j][0].capitalize()

    return cube_string


def solve_cube(faces):
    cube = generate_cube_string(faces)
    return utils.solve(cube.lower(), 'Kociemba')