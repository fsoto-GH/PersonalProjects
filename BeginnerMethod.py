from Cube import Cube
from StandardCubes import StandardCube
from Rubiks import RFace


def solve(cube: Cube):
    _solve_top_layer(cube)
    _solve_middle_layer(cube)
    _solve_last_layer(cube)


def _solve_top_layer(cube):
    # see faces in top layer
    _solve_top_cross(cube)

    pass


def _solve_middle_layer(cube):
    pass


def _solve_last_layer(cube):
    pass

def _solve_top_cross(cube: Cube):
    top_color = cube.faces[RFace.U].color

    l_c = cube.faces[RFace.L].color
    f_c = cube.faces[RFace.F].color
    r_c = cube.faces[RFace.R].color
    b_c = cube.faces[RFace.B].color

    correct = [(top_color, l_c), (top_color, f_c), (top_color, r_c), (top_color, b_c)]

    es = cube.get_edges(top_color)
    wrong_edges = list(filter(lambda x: not (x[2] in correct and x[0][0] == RFace.U), es))
    num_wrong = len(wrong_edges)
    side_correct = sum(1 if cube.faces[e[0][1]].color == e[2][1] else 0 for e in es)

    # consider a solved cross (not orientated)
    if num_wrong == 0 and side_correct != 4:
        if cube.faces[RFace.L].color == cube.faces[RFace.R].color_at(0, 1):
            cube.rotate_up(r=2)
        elif cube.faces[RFace.L].color == cube.faces[RFace.B].color_at(0, 1):
            cube.rotate_up(r=-1)
        else:
            cube.rotate_up()

    while wrong_edges:
        e = wrong_edges[0]
        t_loc = e[0][0]
        turns = ""
        if t_loc != RFace.U:
            if e[0][0] == RFace.D:
                turns = "2"
            elif e[0][0] == RFace.B:
                turns = "'"
            elif e[0][0] == RFace.L:
                # rot = rotate_transform('D')
                turns = "'"
            elif e[0][0] == RFace.R:
                turns = "'"

        print(f'{e[0][1]}{turns}')
        cube.parseRotations(f'{e[0][1]}{turns}')

        es = cube.get_edges(top_color)
        wrong_edges = list(filter(lambda x: not (x[2] in correct and x[0][0] == RFace.U), es))

        print(wrong_edges)

        # if e[0][0] != RFace.U:
        #     if e[1][0] == 1:
        #         r = rotate_transform(e[0][0], "L")
        #         cube.parseRotations(r + "'")


    cube.print_cube()



def rotate_transform(front: str, rotation: str) -> str:
    if front == RFace.F:
        return rotation
    t_dict = {RFace.L: {RFace.U: RFace.U,
                        RFace.D: RFace.D,
                        RFace.L: RFace.B,
                        RFace.R: RFace.F,
                        RFace.F: RFace.L,
                        RFace.B: RFace.R},
              RFace.R: {RFace.U: RFace.U,
                        RFace.D: RFace.D,
                        RFace.L: RFace.F,
                        RFace.R: RFace.B,
                        RFace.F: RFace.R,
                        RFace.B: RFace.L},
              RFace.U: {RFace.U: RFace.B,
                        RFace.D: RFace.F,
                        RFace.L: RFace.L,
                        RFace.R: RFace.R,
                        RFace.F: RFace.U,
                        RFace.B: RFace.D},
              RFace.D: {RFace.U: RFace.F,
                        RFace.D: RFace.B,
                        RFace.L: RFace.L,
                        RFace.R: RFace.R,
                        RFace.F: RFace.D,
                        RFace.B: RFace.U},
              RFace.B: {RFace.U: RFace.U,
                        RFace.D: RFace.D,
                        RFace.L: RFace.R,
                        RFace.R: RFace.L,
                        RFace.F: RFace.B,
                        RFace.B: RFace.F}}

    return t_dict[front][rotation]

if __name__ == '__main__':
    up = 'W'
    front = 'B'
    scramble = "U D2 F2 U' B"

    test = StandardCube()
    test.parseRotations(scramble)
    test.print_cube()
    _solve_top_layer(test)
