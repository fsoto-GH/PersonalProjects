import re
from queue import Queue
from typing import Dict

from CubeFace import CubeFace
from Rubiks import RFace, RMid, RAxis


class Cube:
    def __init__(self, faces: Dict[str: CubeFace], spacing=1):
        if len(faces) != 6:
            raise ValueError("A valid cube requires 6 sides.")

        for face in faces:
            faces[face].spacing = spacing

        self.side_dict = faces

    def rotate_up(self, r=1):
        self.side_dict[RFace.U] = rotate_side(self.side_dict[RFace.U], r)
        self._rotate_layer(RMid.E, r, c=0)

    def rotate_down(self, r=1):
        self.side_dict[RFace.D] = rotate_side(self.side_dict[RFace.D], r)
        self._rotate_layer(RMid.E, -r, c=2)

    def rotate_front(self, r=1):
        self.side_dict[RFace.F] = rotate_side(self.side_dict[RFace.F], r)
        self._rotate_layer(RMid.S, r, c=2)

    def rotate_back(self, r=1):
        self.side_dict[RFace.B] = rotate_side(self.side_dict[RFace.B], r)
        self._rotate_layer(RMid.S, -r, c=0)

    def rotate_left(self, r=1):
        self.side_dict[RFace.L] = rotate_side(self.side_dict[RFace.L], r)
        self._rotate_layer(RMid.M, -r, c=0)

    def rotate_right(self, r=1):
        self.side_dict[RFace.R] = rotate_side(self.side_dict[RFace.R], r)
        self._rotate_layer(RMid.M, r, c=2)

    def rotate_middle(self, r=1):
        self._rotate_mid(RMid.M, r)

    def rotate_equatorial(self, r=1):
        self._rotate_mid(RMid.E, r)

    def rotate_stading(self, r=1):
        self._rotate_mid(RMid.S, r)

    def print_cube(self, spacing=1):
        n = 3

        # top/upper face
        for i in range(n):
            print(f'{" " * (3 * spacing + 2)}  ', end="")
            print(" ".join(f'{j:>{spacing}}' for j in self.side_dict[RFace.U].row(i)))
        print()

        middle_faces = Queue()
        middle_faces.put(self.side_dict[RFace.L])
        middle_faces.put(self.side_dict[RFace.F])
        middle_faces.put(self.side_dict[RFace.R])

        # left, front, and right faces
        for i in range(n):
            for face_row in range(3):
                curr = middle_faces.get()
                middle_faces.put(curr)
                for face in curr.row(i):
                    print(f'{face:>{spacing}}', end=" ")
                print(" ", end="")
            print()
        print()

        # bottom face
        for i in range(n):
            print(f'{" " * (3 * spacing + 2)}  ', end="")
            print(" ".join(f'{j:>{spacing}}' for j in self.side_dict[RFace.D].row(i)))
        print()

        # back face
        for i in range(n):
            print(f'{" " * (3 * spacing + 2)}  ', end="")
            print(" ".join(f'{j:>{spacing}}' for j in self.side_dict[RFace.B].row(i)))

    def __str__(self):
        res = []

        n = self.side_dict[RFace.U].n

        # top/upper face
        for i in range(n):
            res.append(f'{" " * 6} ')
            res.append(" ".join(str(j) for j in self.side_dict[RFace.U].row(i)))
            res.append('\n')
        res.append('\n')

        middle_faces = Queue()
        middle_faces.put(self.side_dict[RFace.L])
        middle_faces.put(self.side_dict[RFace.F])
        middle_faces.put(self.side_dict[RFace.R])

        # left, front, and right faces
        for i in range(n):
            for face_row in range(3):
                curr = middle_faces.get()
                middle_faces.put(curr)
                for face in curr.row(i):
                    res.append(face + " ")
                res.append(" ")
            res.append("\n")
        res.append("\n")

        # bottom face
        for i in range(n):
            res.append(f'{" " * 6} ')
            res.append(" ".join(str(j) for j in self.side_dict[RFace.D].row(i)))
            res.append('\n')
        res.append('\n')

        # back face
        for i in range(n):
            res.append(f'{" " * 6} ')
            res.append(" ".join(str(j) for j in self.side_dict[RFace.B].row(i)))
            res.append('\n')
        res.append('\n')

        return "".join(res)

    def _rotate_mid(self, mid, r=1):
        self._rotate_layer(mid, r, c=1)

    def _rotate_layer(self, diagonal, r=1, c=1):
        """
        This method rotates the center piece from the perspective
        of the front face.

        :param diagonal: which diagonal
        :param r: how many 90 deg. (-) => counter
        :param c: what column, a mid is 1, but variable for simplicity
        :return: None
        """
        if diagonal not in RMid.middles:
            raise ValueError(f"{diagonal} not valid.")
        elif r < -2 or r > 2:
            raise ValueError("Rotations must be between -2 and 2.")

        if not r:
            return

        if r < 0:
            r += 4

        if diagonal == RMid.M:
            n_u = self.side_dict[RFace.F].col(c)
            n_f = self.side_dict[RFace.D].col(c)
            n_d = self.side_dict[RFace.B].col(c)
            n_b = self.side_dict[RFace.U].col(c)
            r -= 1

            while r:
                n_u, n_f, n_d, n_b = n_f, n_d, n_b, n_u
                r -= 1

            self.side_dict[RFace.F].col_set(c, n_f)
            self.side_dict[RFace.D].col_set(c, n_d)
            self.side_dict[RFace.B].col_set(c, n_b)
            self.side_dict[RFace.U].col_set(c, n_u)

        elif diagonal == RMid.E:
            n_b = self.side_dict[RFace.L].row(c, r=True)
            n_l = self.side_dict[RFace.F].row(c)
            n_f = self.side_dict[RFace.R].row(c)
            n_r = self.side_dict[RFace.B].row(2 - c, r=True)
            r -= 1

            while r:
                n_b, n_l, n_f, n_r = n_l[::-1], n_f, n_r, n_b[::-1]
                r -= 1

            self.side_dict[RFace.L].row_set(c, n_l)
            self.side_dict[RFace.F].row_set(c, n_f)
            self.side_dict[RFace.R].row_set(c, n_r)
            self.side_dict[RFace.B].row_set(2 - c, n_b)

        elif diagonal == RMid.S:
            n_u = self.side_dict[RFace.L].col(c, r=True)
            n_l = self.side_dict[RFace.D].row(2 - c)
            n_d = self.side_dict[RFace.R].col(2 - c, r=True)
            n_r = self.side_dict[RFace.U].row(c)
            r -= 1

            while r:
                n_u, n_l, n_d, n_r = n_l[::-1], n_d, n_r[::-1], n_u
                r -= 1

            self.side_dict[RFace.L].col_set(c, n_l)
            self.side_dict[RFace.D].row_set(2 - c, n_d)
            self.side_dict[RFace.R].col_set(2 - c, n_r)
            self.side_dict[RFace.U].row_set(c, n_u)

    def orientate(self, axis: RAxis, r=1):
        """
        This method takes an axis (X, Y, Z) and rotates it.

        :param axis: what axis to rotate from
        :param r: how many 90 deg.
        :return: None
        """
        if r < -2 or r > 2:
            raise ValueError("Rotations must be between -2 and 2.")
        elif axis not in RAxis.axis:
            raise ValueError(f"{axis} is not a valid axis.")

        if axis == RAxis.X:
            self.rotate_left(r=-r)
            self._rotate_mid(RMid.M, r=r)
            self.rotate_right(r=r)
        elif axis == RAxis.Y:
            self.rotate_up(r=r)
            self._rotate_mid(RMid.E, r=r)
            self.rotate_down(r=-r)
        elif axis == RAxis.Z:
            self.rotate_front(r=r)
            self._rotate_mid(RMid.S, r=r)
            self.rotate_back(r=-r)

    def parseRotations(self, s):
        """
        This performs the transformations from a
        space-separated list of rotations. This interprets standard
        Rubik's notation.

        :param s: space-separated values
        :return: None
        """
        rotations = s.split()
        reg = re.compile("^[UFDBLR]2?'?$")
        if all(reg.match(rotation) for rotation in rotations):
            # using function decorators for the face rotations
            rot_dict = {RFace.U: self.rotate_up,
                        RFace.F: self.rotate_front,
                        RFace.D: self.rotate_down,
                        RFace.B: self.rotate_back,
                        RFace.L: self.rotate_left,
                        RFace.R: self.rotate_right}
            for rotation in rotations:
                rot = rotation[0]
                r = 2 if '2' in rotation else 1
                r *= -1 if "'" in rotation else 1
                rot_dict[rot](r)


def rotate_side(side: CubeFace, r):
    """
    This helper-method performs a face rotation for the given side.
    For a rotation [-2, 2], where |r|=1 is 90 and |r|=2 is 180.

    :param side: to rotate from
    :param r: how many 90 deg. (-) => counter
    :return: None
    """
    if r < -2 or r > 2:
        raise ValueError("Rotations must be between -2 and 2.")

    side = [row.copy() for row in side.face]
    if r % 2 == 0:
        return CubeFace([row[::-1] for row in side[::-1]])
    elif r == 1:
        return CubeFace(list(zip(*side[::-1])))
    elif r == -1:
        return CubeFace(list(zip(*side))[::-1])
