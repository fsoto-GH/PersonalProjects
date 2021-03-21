from typing import List

from Rubiks import RColor


class CubeFace:
    def __init__(self, lst: list, spacing: int = 1):
        self.face = lst
        self.spacing = spacing
        self.color = self.face[1][1]

    @property
    def face(self) -> List[list]:
        return self._face

    @face.setter
    def face(self, lst: list) -> None:
        """
        This method takes a size 9 list or 2d 3x3 list and assigns it to
        represent the face. This also sets the color (center 'sticker').

        :param lst: size 9 or 3x3 2d array
        :return: None
        """
        if len(lst) == 9:
            self._face = [[lst[i] for i in range(j, j + 3)] for j in range(0, 9, 3)]
            self.color = lst[4]
        elif len(lst) == 3 and len(set(map(len, lst))) == 1:
            self._face = [list(i) for i in lst]
            # the line below will fix tuple value error, but above works so far
            # self._face = [[lst[i][j] for j in range(0, 3)] for i in range(0, 3)]
            self.color = lst[1][1]
        else:
            raise ValueError("Expected a list size 9 or 2d 3x3 list.")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, v):
        self._color = v

    def row(self, row: int, r: bool = False) -> list:
        return self.face[row][::-1] if r else self.face[row][:]

    def row_set(self, row, n_row):
        for i in range(3):
            self.face[row][i] = n_row[i]

    def col(self, col, r=False):
        return [self.face[2 - i if r else i][col] for i in range(3)]

    def col_set(self, col, n_col):
        for i in range(3):
            self.face[i][col] = n_col[i]

    def color_count(self) -> dict:
        colors = {}
        for color in RColor.colors:
            colors[color] = 0

        for row in self.face:
            for cell in row:
                colors[cell] += 1

        return colors

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, v):
        self._spacing = v

    def __str__(self):
        res = []
        for row in self.face:
            for cell in row:
                res.append(f"{cell:>{self.spacing}} ")
            res.append("\n")

        return "".join(res)
