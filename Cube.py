import re
from queue import Queue
from typing import Dict

from CubeFace import CubeFace
from Rubiks import RFace, RMid, RAxis


class Cube:
    def __init__(self, faces: Dict[RFace, CubeFace], spacing: int = -1):
        if len(faces) != 6:
            raise ValueError("A valid cube requires 6 sides.")
        self.faces = faces
        self.spacing = spacing

    def rotate_up(self, r: int = 1) -> None:
        self.faces[RFace.U] = rotate_side(self.faces[RFace.U], r)
        self._rotate_layer(RMid.E, r, c=0)

    def rotate_down(self, r: int = 1) -> None:
        self.faces[RFace.D] = rotate_side(self.faces[RFace.D], r)
        self._rotate_layer(RMid.E, -r, c=2)

    def rotate_front(self, r: int = 1) -> None:
        self.faces[RFace.F] = rotate_side(self.faces[RFace.F], r)
        self._rotate_layer(RMid.S, r, c=2)

    def rotate_back(self, r: int = 1) -> None:
        self.faces[RFace.B] = rotate_side(self.faces[RFace.B], r)
        self._rotate_layer(RMid.S, -r, c=0)

    def rotate_left(self, r: int = 1) -> None:
        self.faces[RFace.L] = rotate_side(self.faces[RFace.L], r)
        self._rotate_layer(RMid.M, -r, c=0)

    def rotate_right(self, r: int = 1) -> None:
        self.faces[RFace.R] = rotate_side(self.faces[RFace.R], r)
        self._rotate_layer(RMid.M, r, c=2)

    def rotate_middle(self, r: int = 1) -> None:
        self._rotate_mid(RMid.M, r)

    def rotate_equatorial(self, r: int = 1) -> None:
        self._rotate_mid(RMid.E, r)

    def rotate_standing(self, r: int = 1) -> None:
        self._rotate_mid(RMid.S, r)

    def print_cube(self):
        """
        This method prints the entire cube's net drawing, where
        the intersection represents the front face.

        :return: None
        """
        n = 3

        for i in range(n):
            print(f'{" " * (n * self.spacing + 2)}  ', end="")
            print(" ".join(f'{j:>{self.spacing}}' for j in self.faces[RFace.U].row(i)))
        print()

        middle_faces = Queue()
        middle_faces.put(self.faces[RFace.L])
        middle_faces.put(self.faces[RFace.F])
        middle_faces.put(self.faces[RFace.R])

        # left, front, and right faces
        for i in range(n):
            for face_row in range(n):
                curr = middle_faces.get()
                middle_faces.put(curr)
                for face in curr.row(i):
                    print(f'{face:>{self.spacing}}', end=" ")
                print(" ", end="")
            print()
        print()

        # bottom face
        for i in range(n):
            print(f'{" " * (n * self.spacing + 2)}  ', end="")
            print(" ".join(f'{j:>{self.spacing}}' for j in self.faces[RFace.D].row(i)))
        print()

        # back face
        for i in range(n):
            print(f'{" " * (n * self.spacing + 2)}  ', end="")
            print(" ".join(f'{j:>{self.spacing}}' for j in self.faces[RFace.B].row(i)))

    def __str__(self):
        res = []
        n = 3
        # top/upper face
        for i in range(n):
            res.append(f'{" " * 6} ')
            res.append(" ".join(str(j) for j in self.faces[RFace.U].row(i)))
            res.append('\n')
        res.append('\n')

        middle_faces = Queue()
        middle_faces.put(self.faces[RFace.L])
        middle_faces.put(self.faces[RFace.F])
        middle_faces.put(self.faces[RFace.R])

        # left, front, and right faces
        for i in range(n):
            for face_row in range(n):
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
            res.append(" ".join(str(j) for j in self.faces[RFace.D].row(i)))
            res.append('\n')
        res.append('\n')

        # back face
        for i in range(n):
            res.append(f'{" " * 6} ')
            res.append(" ".join(str(j) for j in self.faces[RFace.B].row(i)))
            res.append('\n')
        res.append('\n')

        return "".join(res)

    def _rotate_mid(self, mid, r:int = 1) -> None:
        """
        This (private) method rotates the middle layer.

        :param mid: what middle to rotate
        :param r: how many 90 deg. (-) => counter
        :return: None
        """
        self._rotate_layer(mid, r, c=1)

    def _rotate_layer(self, diagonal: RMid, r: int = 1, c: int = 1) -> None:
        """
        This (private) method rotates a Rubik's layer from the perspective of
        the front. By default, the middle layer is rotated; however, the
        row and column can be specified.

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
            n_u = self.faces[RFace.F].col(c)
            n_f = self.faces[RFace.D].col(c)
            n_d = self.faces[RFace.B].col(c)
            n_b = self.faces[RFace.U].col(c)
            r -= 1

            while r:
                n_u, n_f, n_d, n_b = n_f, n_d, n_b, n_u
                r -= 1

            self.faces[RFace.F].col_set(c, n_f)
            self.faces[RFace.D].col_set(c, n_d)
            self.faces[RFace.B].col_set(c, n_b)
            self.faces[RFace.U].col_set(c, n_u)

        elif diagonal == RMid.E:
            n_b = self.faces[RFace.L].row(c, r=True)
            n_l = self.faces[RFace.F].row(c)
            n_f = self.faces[RFace.R].row(c)
            n_r = self.faces[RFace.B].row(2 - c, r=True)
            r -= 1

            while r:
                n_b, n_l, n_f, n_r = n_l[::-1], n_f, n_r, n_b[::-1]
                r -= 1

            self.faces[RFace.L].row_set(c, n_l)
            self.faces[RFace.F].row_set(c, n_f)
            self.faces[RFace.R].row_set(c, n_r)
            self.faces[RFace.B].row_set(2 - c, n_b)

        elif diagonal == RMid.S:
            n_u = self.faces[RFace.L].col(c, r=True)
            n_l = self.faces[RFace.D].row(2 - c)
            n_d = self.faces[RFace.R].col(2 - c, r=True)
            n_r = self.faces[RFace.U].row(c)
            r -= 1

            while r:
                n_u, n_l, n_d, n_r = n_l[::-1], n_d, n_r[::-1], n_u
                r -= 1

            self.faces[RFace.L].col_set(c, n_l)
            self.faces[RFace.D].row_set(2 - c, n_d)
            self.faces[RFace.R].col_set(2 - c, n_r)
            self.faces[RFace.U].row_set(c, n_u)

    def orientate(self, axis: RAxis, r: int = 1) -> None:
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

    def parseRotations(self, s: str) -> None:
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

    @property
    def faces(self) -> Dict[RFace, CubeFace]:
        return self._faces

    @faces.setter
    def faces(self, faces: Dict[RFace, CubeFace]) -> None:
        self._faces = faces

    @property
    def spacing(self) -> int:
        return self._spacing

    @spacing.setter
    def spacing(self, s: int) -> None:
        """
        This method sets the printing spacing.
        If none or a negative spacing is specified, it will
        set the spacing to the length of the longest 'sticker.'

        :param s: spacing int
        :return: None
        """
        if s < 0 or type(s) != int:
            s = 1
            for face in self.faces:
                for cell in self.faces[face].face:
                    s = s if s > len(str(cell)) else s
            print(s)

        for face in self.faces:
            self.faces[face].spacing = s

        self._spacing = s


def rotate_side(side: CubeFace, r: int) -> CubeFace:
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