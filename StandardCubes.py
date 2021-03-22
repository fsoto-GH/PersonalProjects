from Cube import Cube
from CubeFace import CubeFace
from RColors import RColors
from Rubiks import RFace


class StandardCube(Cube):
    """
    This is a standard, solved cube with the white face up
    and blue face front.
    """

    def __init__(self):
        u = CubeFace(['W' for _ in range(9)])
        f = CubeFace(['B' for _ in range(9)])
        d = CubeFace(['Y' for _ in range(9)])
        b = CubeFace(['G' for _ in range(9)])
        l = CubeFace(['R' for _ in range(9)])
        r = CubeFace(['O' for _ in range(9)])

        super().__init__({RFace.U: u,
                          RFace.F: f,
                          RFace.D: d,
                          RFace.B: b,
                          RFace.L: l,
                          RFace.R: r}, spacing=1)


class NumberedCube(Cube):
    """
    This is a standard, solved cube numbered 1-54.
    The order of numbers goes across from U-L-F-R-B-D.
    This should only be used for testing and not for actual solving.
    """

    def __init__(self):
        u = CubeFace([i for i in range(1, 10)])
        l = CubeFace([i for i in range(10, 19)])
        f = CubeFace([i for i in range(19, 28)])
        r = CubeFace([i for i in range(28, 37)])
        b = CubeFace([i for i in range(37, 46)])
        d = CubeFace([i for i in range(46, 55)])

        super().__init__({RFace.U: u,
                          RFace.F: f,
                          RFace.D: d,
                          RFace.B: b,
                          RFace.L: l,
                          RFace.R: r}, spacing=2)


class StandardFaced(Cube):
    """
    This is a standard cube with 'stickers' being the letter
    of the face they belong to.
    """
    def __init__(self):
        u = CubeFace([f'{RFace.U}' for _ in range(1, 10)])
        f = CubeFace([f'{RFace.F}' for _ in range(10, 19)])
        d = CubeFace([f'{RFace.D}' for _ in range(19, 28)])
        b = CubeFace([f'{RFace.B}' for _ in range(28, 37)])
        l = CubeFace([f'{RFace.L}' for _ in range(37, 46)])
        r = CubeFace([f'{RFace.R}' for _ in range(46, 55)])

        colors = {RFace.U: RFace.U,
                  RFace.L: RFace.L,
                  RFace.F: RFace.F,
                  RFace.R: RFace.R,
                  RFace.B: RFace.B,
                  RFace.D: RFace.D}

        ring = {RFace.F: RFace.R,
                RFace.R: RFace.B,
                RFace.B: RFace.L,
                RFace.L: RFace.F}

        complements = {RFace.F: RFace.B,
                       RFace.B: RFace.F,
                       RFace.R: RFace.L,
                       RFace.L: RFace.R,
                       RFace.U: RFace.D,
                       RFace.D: RFace.U}

        poles = {'U': RFace.U,
                 'D': RFace.D}

        colors = RColors(colors=colors, complements=complements, ring=ring, poles=poles)

        super().__init__({RFace.U: u,
                          RFace.F: f,
                          RFace.D: d,
                          RFace.B: b,
                          RFace.L: l,
                          RFace.R: r}, spacing=2, colors=colors)

    # def orientate(self, up: str, front: str) -> None:
    #     super().__init__()
