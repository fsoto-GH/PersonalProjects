import unittest

from StandardCubes import StandardCube


class MyTestCase(unittest.TestCase):
    def test_s1(self):
        test = StandardCube()
        test.orientate('Y', 'G')
        test.parseRotations(
            "R U' D B F2 R2 B D' U F2 R2 B L' F' L R' D2 F' U' D2 B' D' L2 B L B2 D' F2 R2 F2 D' F D' R' U R2 U2 F2 "
            "B' D' U' F' B2 U' B' R L B2 F U' L2 F' D U' L D B2 U2 R2 L2 U2 F' U' L' B2 F2 L B L2 B2 U2 B' F U' F D "
            "F' L' R' B' F2 U2 R2 F2 B U' L2 F' R' D B U' B2 R' F2 B2 L B D' R")

        res = """       O B Y
       Y Y Y
       O R G

Y G W  B W R  W B R  G O B
R R R  G G W  G O B  W B B
R O O  G R W  G O B  R Y Y

       Y Y O
       G W W
       B O W"""
        self.assertEqual(res, str(test), 'S1 failed')

    def test_s2(self):
        test = StandardCube()
        test.orientate('G', 'Y')
        test.parseRotations(
            "R U R2 D2 B2 L B' L' B' D' B2 D2 L R' F' R' U' D F' B2 R U' L' B U' B R2 F D R' L2 D2 U R2 L2 U L2 R2 D' "
            "L' B F' L' D L' U B R' D' R L2 F' R' B2 D R F' L2 F' B' R2 B F' R2 L' B F2 L2 B F' D U' L2 D' L2 U B2 U' "
            "L U' F' R' B' F' R2 U' R2 D2 F D2 B U2 R2 D2 F D' B L R' D2")

        res = """       O B Y
       O G G
       O O B

B W G  W B W  R R R  G R W
O O O  G Y R  W R G  Y W Y
O G R  G B O  G B Y  R Y B

       W W Y
       W B Y
       Y R B"""
        self.assertEqual(res, str(test), 'S2 failed')

    def test_s3(self):
        test = StandardCube()
        test.orientate('O', 'Y')
        test.parseRotations("L R U' F' R F' U2 D' B R' D2 L D B' U2 B R2 L' U B")

        res = """       O W W
       B O Y
       O B G

G O G  W R R  W O R  B O Y
Y B G  O Y R  W G W  B W R
Y Y B  Y G B  W G O  Y B R

       R R O
       G R W
       G Y B"""
        self.assertEqual(res, str(test), 'S3 failed')

    def test_s4(self):
        test = StandardCube()
        test.orientate('W', 'B')
        test.parseRotations("R' U' R' B2 F' L2 U' B' R' F B2 R2 U L2 F' L' F2 U L' R")
        U = [['G', 'Y', 'R'],
             ['B', 'W', 'O'],
             ['O', 'R', 'B']]

        self.assertEqual(test.faces['U'].face, U, 'S4 failed')


if __name__ == '__main__':
    unittest.main()
