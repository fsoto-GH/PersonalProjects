import unittest

import kociemba

from StandardCubes import StandardCube


class MyTestCase(unittest.TestCase):
    def test_scrambles(self):
        scrambles = [('Y', 'B', "L2 U D' R U' D' L2 R2 F' U R2 L D R' L U' R2 U D2 R2 B' R U D' L2"),
                     ('O', 'G', "U' B2 F' R' D U2 R2 D' F' R' D2 L' F2 R L B R2 U' R' U R' B2 F U2 B'"),
                     ('Y', 'B', "D' F' D B' L U F2 U' R L' U' B2 R F B2 U D2 B F L' D2 L2 B F U2 R D2 U2 B2 L R' B R' U' D F2 B2 L' B' D' U L' F' D L' U' L2 U2 B F2"),
                     ('O', 'B', "D' F2 D R F2 D2 B D' L B L B2 D B F D' L2 B' R B R' F' R' F2 B2 R' U' R2 B U' L' B U B D2 R L2 B' R F2 D' F B2 R B' L R D2 L2 B2"),
                     ('Y', 'R', "B L' F R' D2 B2 F' R' D L R2 F2 R U2 F D2 U L B2 L' D2 U F' B2 R2 B U' D' B2 L' F' B D2 R U2 L U' F' L F' U' R D' B2 D' F2 D2 U L' D' L2 R2 F D F2 D L' R' F D2 B L' D' L' U' L U2 D2 R B2 L' B2 L' B R'"),
                     ('W', 'B', "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2")]

        for i, scramble in enumerate(scrambles, 1):
            self.scramble_assert(scramble[0], scramble[1], scramble[2], i)

    def scramble_assert(self, u, f, scramble, s_n):
        test = StandardCube()
        test.orientate(u, f)
        test.parseRotations(scramble)

        # check is_solved correctly checks unsolved
        self.assertEqual(test.is_solved, False, f'S{s_n} failed checking unsolved')

        sol = kociemba.solve(test.ubl, test.ubl_solved)
        test.parseRotations(sol)

        # check is_solved correctly checks solved
        self.assertEqual(test.is_solved, True, f'S{s_n} failed checking solved')


if __name__ == '__main__':
    unittest.main()
