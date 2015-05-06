from loader import config
import dhmatrix
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class robotArm:

    def __init__(self):
        self.joint = config.joint
        self.hasChanged = True
        self.updateAllTransformer()
        self.updateAllState()

    def draw(self):
        glPushMatrix()
        glColor3f(0.0, 1.0, 0.0)
        last = None
        quadratic = gluNewQuadric()

        for j in self.joint:
            glColor3f(1.0, 0.0, 0.0)
            glPushMatrix()
            glRotated(math.degrees(j.theta), 0, 0, 1)
            glMaterial(GL_FRONT, GL_AMBIENT, [0.0, 1.0, 0.0, 1.0])
            # glColor3f(0, 1, 0)
            if j.d < 0.02:
                gluCylinder(quadratic, 0.04, 0.04, 0.02, 10, 10)
            else:
                gluCylinder(quadratic, 0.04, 0.04, j.d, 10, 10)
            glTranslated(0, 0, j.d)

            glColor3f(1.0, 0.0, 0.0)
            glPopMatrix()
            glMultMatrixd(j.iniM().transD().rotTheta().transR().m.transpose())

            glPushMatrix()
            glRotatef(-90, 0, 1, 0)
            glMaterial(GL_FRONT, GL_AMBIENT, [0.0, 0.0, 1.0, 1.0])
            if j.r < 0.02:
                gluCylinder(quadratic, 0.02, 0.02, 0.02, 10, 10)
            else:
                gluCylinder(quadratic, 0.02, 0.02, j.r, 10, 10)
            glPopMatrix()

            glMultMatrixd(j.iniM().rotAlpha().m.transpose())
            last = j

        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glRotated(math.degrees(last.theta), 0, 0, 1)
        glColor3f(0, 1, 0)
        gluCylinder(quadratic, 0.04, 0.04, last.d, 10, 10)
        glPopMatrix()

        glPopMatrix()

    def slowTo(self, jointAngles):
        for 
        self.joint

    def updateAllTransformer(self):
        self.transformer = []
        for m in self.joint:
            self.transformer.append(m.transform())
            self.hasChanged = True

    def updateAllState(self):
        if not self.hasChanged:
            return
        currentState = None
        self.states = []
        for trans in self.transformer:
            if currentState is None:
                currentState = trans
                self.states.append(currentState)
            else:
                currentState = currentState * trans
                self.states.append(currentState)
                print currentState[(0, 3)]
        self.hasChanged = False