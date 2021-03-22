import re
from queue import Queue
from typing import Dict, Union

from CubeFace import CubeFace
from RColors import RColors, StandardRColors
from Rubiks import RFace, RMid, RAxis


class Cube:
    def __init__(self, faces: Dict[Union[RFace, str], CubeFace], spacing: int = -1,
                 colors: RColors = StandardRColors()):
        if len(faces) != 6:
            raise ValueError("A valid cube requires 6 sides.")
        self.faces = faces
        self.spacing = spacing
        self.colors = colors.colors
        self.ring = colors.ring
        self.complements = colors.complements
        self.poles = colors.poles

    def rotate_up(self, r: int = 1) -> None:
        self._rotate_face(RFace.U, r)
        self._rotate_layer(RMid.E, r, c=0)

    def rotate_down(self, r: int = 1) -> None:
        self._rotate_face(RFace.D, r)
        self._rotate_layer(RMid.E, -r, c=2)

    def rotate_front(self, r: int = 1) -> None:
        self._rotate_face(RFace.F, r)
        self._rotate_layer(RMid.S, r, c=2)

    def rotate_back(self, r: int = 1) -> None:
        self._rotate_face(RFace.B, r)
        self._rotate_layer(RMid.S, -r, c=0)

    def rotate_left(self, r: int = 1) -> None:
        self._rotate_face(RFace.L, r)
        self._rotate_layer(RMid.M, r, c=0)

    def rotate_right(self, r: int = 1) -> None:
        self._rotate_face(RFace.R, r)
        self._rotate_layer(RMid.M, -r, c=2)

    def rotate_middle(self, r: int = 1) -> None:
        self._rotate_mid(RMid.M, r)

    def rotate_equatorial(self, r: int = 1) -> None:
        self._rotate_mid(RMid.E, r)

    def rotate_standing(self, r: int = 1) -> None:
        self._rotate_mid(RMid.S, r)

    def rotate_X(self, r: int = 1) -> None:
        self._orientate_axis(RAxis.X, r)

    def rotate_Y(self, r: int = 1) -> None:
        self._orientate_axis(RAxis.Y, r)

    def rotate_Z(self, r: int = 1) -> None:
        self._orientate_axis(RAxis.Z, r)

    def print_cube(self) -> None:
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
        middle_faces.put(self.faces[RFace.B])

        # left, front, and right faces
        for i in range(n):
            for face_row in range(4):
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
        middle_faces.put(self.faces[RFace.B])

        # left, front, and right faces
        for i in range(n):
            for face in range(4):
                curr = middle_faces.get()
                middle_faces.put(curr)
                for j, cell in enumerate(curr.row(i)):
                    res.append(cell + (" " if face * 3 + j != 11 else ""))
                res.append(" " if face != 3 else "")
            res.append("\n")
        res.append("\n")

        # bottom face
        for i in range(n):
            res.append(f'{" " * 6} ')
            res.append(" ".join(str(j) for j in self.faces[RFace.D].row(i)))
            res.append('\n' if i != n - 1 else "")
        res.append('\n' if i != n - 1 else "")

        return "".join(res)

    def parseRotations(self, s: str) -> None:
        """
        This performs the transformations from a
        space-separated list of rotations. This interprets standard
        Rubik's notation.

        :param s: space-separated values
        :return: None
        """
        rotations = s.split()
        reg = re.compile("^[UFDBLRMESXYZ]2?'?$")
        if all(reg.match(rotation) for rotation in rotations):
            # using function decorators for the face rotations
            rot_dict = {RFace.U: self.rotate_up,
                        RFace.F: self.rotate_front,
                        RFace.D: self.rotate_down,
                        RFace.B: self.rotate_back,
                        RFace.L: self.rotate_left,
                        RFace.R: self.rotate_right,
                        RMid.M: self.rotate_middle,
                        RMid.E: self.rotate_equatorial,
                        RMid.S: self.rotate_standing,
                        RAxis.X: self.rotate_X,
                        RAxis.Y: self.rotate_Y,
                        RAxis.Z: self.rotate_Z}
            for rotation in rotations:
                rot = rotation[0]
                r = 2 if '2' in rotation else 1
                r *= -1 if "'" in rotation else 1
                rot_dict[rot](r)

    def orientate(self, up: str, front: str) -> None:
        """
        This method reorientates the perspective faces.

        :param up: face color to be up face
        :param front: face color to be the front face
        :param ring: what ring to use
        :return: None
        """
        # find the faces and mark
        n_u = self.faces[self.find_face(up)].face
        n_f = self.faces[self.find_face(front)].face
        n_d = self.faces[self.find_face(self.complements[up])].face
        n_b = self.faces[self.find_face(self.complements[front])].face

        try:
            if up in self.ring and front in self.ring:
                # considers edge case where ring composes the up and front
                if self.ring[up] == front:
                    n_r = self.faces[self.find_face(self.poles['U'])].face
                    n_l = self.faces[self.find_face(self.poles['D'])].face
                else:
                    n_r = self.faces[self.find_face(self.poles['D'])].face
                    n_l = self.faces[self.find_face(self.poles['U'])].face
            else:
                # whether the ring is upside or downside
                if up in self.ring:
                    if front == self.poles['U']:
                        l = self.find_face(self.ring[up])
                        n_l = self.faces[l].face
                        r = self.find_face(self.complements[self.faces[l].color])
                        n_r = self.faces[r].face
                    else:
                        r = self.find_face(self.ring[up])
                        n_r = self.faces[r].face
                        l = self.find_face(self.complements[self.faces[r].color])
                        n_l = self.faces[l].face
                else:
                    if up == self.poles['U']:
                        r = self.find_face(self.ring[front])
                        n_r = self.faces[r].face
                        l = self.find_face(self.complements[self.faces[r].color])
                        n_l = self.faces[l].face
                    else:
                        l = self.find_face(self.ring[front])
                        n_l = self.faces[l].face
                        r = self.find_face(self.complements[self.faces[l].color])
                        n_r = self.faces[r].face

        except KeyError as ke:
            raise KeyError("Not a valid cube!") from ke

        self.faces[RFace.U].face = n_u
        self.faces[RFace.F].face = n_f
        self.faces[RFace.D].face = n_d
        self.faces[RFace.B].face = n_b
        self.faces[RFace.L].face = n_l
        self.faces[RFace.R].face = n_r

    def find_face(self, color: str) -> Union[RFace, str]:
        """
        This method returns the face orientation of a given color.

        :param color: center color to look for
        :return: None
        """
        for face in self.faces:
            if self.faces[face].color == color:
                return face
        raise ValueError(f"{color} not in cube.")

    def _rotate_mid(self, mid, r: int = 1) -> None:
        """
        This (private) method rotates the middle layer.

        :param mid: what middle to rotate
        :param r: how many 90 deg. (-) => counter
        :return: None
        """
        self._rotate_layer(mid, r, c=1)

    def _rotate_layer(self, diagonal: Union[RMid, str], r: int = 1, c: int = 1) -> None:
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
        elif abs(r) != 1 and abs(r) != 2:
            raise ValueError("Rotation, r, must be |r| = [1, 2]")

        if r < 0:
            r += 4

        if diagonal == RMid.M:
            n_u = self.faces[RFace.B].col(2 - c, r=True)
            n_b = self.faces[RFace.D].col(c, r=True)
            n_d = self.faces[RFace.F].col(c)
            n_f = self.faces[RFace.U].col(c)
            r -= 1

            while r:
                n_u, n_b, n_d, n_f = n_b[::-1], n_d[::-1], n_f, n_u
                r -= 1

            self.faces[RFace.B].col_set(2 - c, n_b)
            self.faces[RFace.D].col_set(c, n_d)
            self.faces[RFace.F].col_set(c, n_f)
            self.faces[RFace.U].col_set(c, n_u)

        elif diagonal == RMid.E:
            n_b = self.faces[RFace.L].row(c)
            n_l = self.faces[RFace.F].row(c)
            n_f = self.faces[RFace.R].row(c)
            n_r = self.faces[RFace.B].row(c)
            r -= 1

            while r:
                n_b, n_l, n_f, n_r = n_l, n_f, n_r, n_b
                r -= 1

            self.faces[RFace.L].row_set(c, n_l)
            self.faces[RFace.F].row_set(c, n_f)
            self.faces[RFace.R].row_set(c, n_r)
            self.faces[RFace.B].row_set(c, n_b)

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

    def _rotate_face(self, side: Union[RFace, str], r: int = 1) -> None:
        """
        This (private) method rotates a face by a given amount |r| = [1, 2]
        :param side:
        :param r:
        :return:
        """
        if abs(r) != 1 and abs(r) != 2:
            raise ValueError("Rotation, r, must be |r| = [1, 2]")

        side = self.faces[side]

        if r == 1:
            side.face = list(zip(*side.face[::-1]))
        elif r == -1:
            side.face = list(zip(*side.face))[::-1]
        else:
            side.face = [row[::-1] for row in side.face[::-1]]

    def _orientate_axis(self, axis: RAxis, r: int = 1) -> None:
        """
        This (private) method takes an axis (X, Y, Z) and rotates it.

        :param axis: what axis to rotate from
        :param r: how many 90 deg |r| = [1, 2]
        :return: None
        """
        if abs(r) != 1 and abs(r) != 2:
            raise ValueError("Rotation, r, must be |r| = [1, 2]")
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

    @property
    def faces(self) -> Dict[Union[RFace, str], CubeFace]:
        return self._faces

    @faces.setter
    def faces(self, faces: Dict[Union[RFace, str], CubeFace]) -> None:
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
                    n_s = len(str(cell))
                    s = s if s > n_s else n_s

        for face in self.faces:
            self.faces[face].spacing = s

        self._spacing = s

    @property
    def is_solved(self):
        """
        :return: a boolean indicate if cube is solved
        """
        return all(len(self.faces[face].color_count()) == 1 for face in self.faces)

    @property
    def ubl(self):
        """
        :return: a UBL string of the current cube state
        """
        res = []
        o_d = self.orientation_dict
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            for face_row in self.faces[face].face:
                for cell in face_row:
                    res.append("".join(o_d[cell]))

        return "".join(res)

    @property
    def ubl_solved(self) -> str:
        """
        :return: a UBL string that represents the solved cub
        """
        res = []
        o_d = self.orientation_dict
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            o = o_d[self.faces[face].color]
            res.append("".join(f"{o}" for _ in range(9)))
        return "".join(res)

    @property
    def orientation_dict(self) -> dict:
        """
        :return: a dictionary with keys being the color of each face
        and values being the matching RFace.
        """
        o_d = {}
        for face in RFace.faces:
            o_d[self.faces[face].color] = face

        return o_d
