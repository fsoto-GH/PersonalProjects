from Rubiks import RFace


class RColors:
    def __init__(self, colors=None, complements=None, ring=None, poles=None):
        self.colors = colors
        self.complements = complements
        self.ring = ring
        self.poles = poles


class StandardRColors(RColors):
    """
    This class contains the 6 standard colors of a Rubik's cube.
    There is also a dictionary for quick exception handling.
    """

    def __init__(self):
        R = 'R'
        G = 'G'
        B = 'B'
        W = 'W'
        Y = 'Y'
        O = 'O'
        colors = {R: R,
                  G: G,
                  B: B,
                  W: W,
                  Y: Y,
                  O: O}

        complements = {R: O,
                       O: R,
                       G: B,
                       B: G,
                       W: Y,
                       Y: W}

        ring = {R: B,
                B: O,
                O: G,
                G: R}

        poles = {RFace.U: W,
                 RFace.D: Y}

        super().__init__(colors=colors, complements=complements, ring=ring, poles=poles)
