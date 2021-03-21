from StandardCubes import NumberedCube, StandardCube
test = NumberedCube()

for rotation in "U2 L' U' F R D2 U L2 U R U' D L2 F' D L2 U' L D' R' B2 F' L2 B2 L'".split():
    print(rotation)
    test.parseRotations(rotation)
    test.print_cube()

print(test.side_dict['U'])

