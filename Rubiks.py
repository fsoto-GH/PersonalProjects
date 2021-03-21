"""
This contains common Rubik's terms.
This is used to facilitate and maintain concurrency across
classes.
"""


class RColor:
    """
    This class contains the 6 standard colors of a Rubik's cube.
    There is also a dictionary for quick exception handling.
    """
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


class RFace:
    """
    This class contains the 6 standard faces of a Rubik's cube.
    There is also a dictionary for quick exception handling.
    """
    U = 'U'
    F = 'F'
    D = 'D'
    B = 'B'
    L = 'L'
    R = 'R'

    faces = {U: U,
             F: F,
             D: D,
             B: B,
             L: L,
             R: R}


class RMid:
    """
    This class contains the 3 standard middle rotations of a Rubik's cube.
    There is also a dictionary for quick exception handling.
    """
    S = 'S'
    E = 'E'
    M = 'M'

    middles = {S: S,
               E: E,
               M: M}


class RAxis:
    """
    This class contains the 3 standard rotations of a Rubik's cube.
    There is also a dictionary for quick exception handling.
    """
    X = 'X'
    Y = 'Y'
    Z = 'Z'

    axis = {X: X,
            Y: Y,
            Z: Z}
