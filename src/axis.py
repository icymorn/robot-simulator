from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class WorldAxis:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def draw(self):
        glPushMatrix()
        glPushAttrib(GL_LIGHTING_BIT)

        glTranslatef(self.x, self.y, self.z)
        # glLoadIdentity()
        # Draw the x-axis in red.
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1], 0)
        glPushMatrix()
        glRotatef(90, 0, 1, 0) # drawAxis draws a z-axis; rotate it onto the x-axis.
        glColor3f(1, 0, 0)
        self._drawAxis()
        glPopMatrix()

        # Draw the y-axis in green.

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 0.8, 0, 1], 0)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0) # drawAxis draws a z-axis; rotate it onto the y-axis.
        glColor3f(0, 1, 0)
        self._drawAxis()
        glPopMatrix()

        # Draw the z-axis in blue.
        glPushMatrix()
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.2, 0.2, 1, 1], 0)
        glColor3f(0, 0, 1)
        self._drawAxis()
        glPopMatrix()

        glPopAttrib()
        glPopMatrix()

    def _drawAxis(self):
        # glPushMatrix()
        q = gluNewQuadric()
        #Cylinder, radius 0.02, height 1, base at (0,0,0), lying on z-axis.
        gluCylinder(q, 0.02, 0.02, 1, 4, 4)
        # Move the cone to the top of the cylinder
        glTranslatef(0, 0, 1)
        # Cone, radius 0.1, height 0.3, base at (0,0,0), pointing along z-axis.
        glutSolidCone(0.1, 0.3, 12, 5)
        # glPopMatrix()
