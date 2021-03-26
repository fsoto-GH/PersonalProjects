from typing import List, Union, Dict


class CubeFace:
    def __init__(self, lst: list, spacing: int = 1):
        self.face = lst
        self.spacing = spacing
        self.color = self.face[1][1]

    @property
    def face(self) -> List[list]:
        return self._face

    @face.setter
    def face(self, lst: Union[List[List], list]) -> None:
        """
        This method takes a size 9 list or 2d 3x3 list and assigns it to
        represent the face. This also sets the color (center 'sticker').

        :param lst: size 9 or 3x3 2d array
        :return: None
        """
        if len(lst) == 9:
            self._face = [lst[:3], lst[3:6], lst[6:]]
            self.color = lst[4]
        elif len(lst) == 3 and len(set(map(len, lst))) == 1:
            self._face = [list(i) for i in lst]
            # the line below will fix tuple value error, but above works so far
            # self._face = [[lst[i][j] for j in range(0, 3)] for i in range(0, 3)]
            self.color = lst[1][1]
        else:
            raise ValueError("Expected a list size 9 or 2d 3x3 list.")

    def find_color(self, color: str, center: bool = False) -> List[tuple]:
        """
        Looks for a particular color in the face.

        :param color: color to look for
        :param center: whether the center should be considered
        :return:
        """

        coords = []
        for i, face_row in enumerate(self.face):
            for j, cell in enumerate(face_row):
                if cell == color:
                    if not center and i == j:
                        continue

                    coords.append((i, j))

        return coords

    def color_at(self, r: int, c: int) -> str:
        return self.face[r][c]

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, v):
        self._color = v

    def row(self, row: int, r: bool = False) -> list:
        """
        :param row: int [0, 2]
        :param r: boolean indicating if reversed
        :return: list containing a copy of the row
        """
        return self.face[row][::-1] if r else self.face[row][:]

    def row_set(self, row, n_row):
        for i in range(3):
            self.face[row][i] = n_row[i]

        if row == 1:
            self.color = self.face[1][1]

    def col(self, col, r=False) -> list:
        """
        :param col: int [0, 2]
        :param r: boolean indicating if reversed
        :return: list containing a copy of the col
        """
        return [self.face[2 - i if r else i][col] for i in range(3)]

    def col_set(self, col, n_col):
        for i in range(3):
            self.face[i][col] = n_col[i]
        if col == 1:
            self.color = self.face[1][1]

    def color_count(self) -> Dict[str, int]:
        """
        This returns a dictionary containing the count
        of colors in the face.

        :return: color count dictionary
        """
        color_count = {}
        for color in sum(self.face, []):
            if color in color_count:
                color_count[color] += 1
            else:
                color_count[color] = 1

        return color_count

    @property
    def spacing(self) -> int:
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

