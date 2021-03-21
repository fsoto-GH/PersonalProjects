# Rubiks

<p>This repository contains my shot at a mechanical 3x3 Rubik's cube solver.</p>

<p>This contains the following classes:</p>
<ul>
    <li>Cube</li>
    <li>CubeFace</li>
    <li>StandardCubes</li>
    <li>Rubiks</li>
</ul>

The <b>Rubiks</b> file contains three classes which consist of standard Rubik's notation. Such as the face names (<i>
RFace</i>), middle rotations (<i>RMid</i>), axial rotations (<i>RAxis</i>), and 'sticker' colors (<i>RColor</i>).

However, it is not necessary to import as they are means to reduce and avoid concurrency issues. For example, RMid.F can
be replaced with 'F' and RAxis.X can be replaced with 'X'. Additionally, RColor can be modified to different colors.

<p>The <b>Cube</b> is the container and represents a Rubik's cube. 
To create an instance, a dictionary (RFace: CubeFace), containing the six faces, is expected.
The purpose of the class is to perform standard Rubik's rotations.

