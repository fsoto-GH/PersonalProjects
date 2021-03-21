from Cube import Cube
from Rubiks import RColor, RFace
from CubeFace import CubeFace


class StandardCube(Cube):
    """
    This is a standard, solved cube with the white face up
    and blue face front.
    """

    def __init__(self):
        u = CubeFace([RColor.W for _ in range(9)])
        f = CubeFace([RColor.B for _ in range(9)])
        d = CubeFace([RColor.Y for _ in range(9)])
        b = CubeFace([RColor.G for _ in range(9)])
        l = CubeFace([RColor.R for _ in range(9)])
        r = CubeFace([RColor.O for _ in range(9)])

        super().__init__({RFace.U: u,
                          RFace.F: f,
                          RFace.D: d,
                          RFace.B: b,
                          RFace.L: l,
                          RFace.R: r})


class NumberedCube(Cube):
    def __init__(self):
        u = CubeFace([i for i in range(1, 10)])
        f = CubeFace([i for i in range(10, 19)])
        d = CubeFace([i for i in range(19, 28)])
        b = CubeFace([i for i in range(28, 37)])
        l = CubeFace([i for i in range(37, 46)])
        r = CubeFace([i for i in range(46, 55)])

        super().__init__({RFace.U: u,
                          RFace.F: f,
                          RFace.D: d,
                          RFace.B: b,
                          RFace.L: l,
                          RFace.R: r}, spacing=2)

    def print_cube(self, spacing=2):
        super().print_cube(spacing)
