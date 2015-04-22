from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class GridPlane:
    def __init__(self, row = 8, col = 8, x = -8, y = -8, z = 0):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.z = z

    def draw(self):
        glPushMatrix()
        glLineWidth(2)
        glColor3f(0.5, 0.5, 0.5)
        glTranslatef(self.x, self.y, self.z)
        glBegin(GL_LINES)

        for i in range(self.row):
            glVertex2f(0, i)
            glVertex2f(self.col, i)

        for i in range(self.col):
            glVertex2f(i, 0)
            glVertex2f(i, self.row)

        glEnd()
        glPopMatrix()