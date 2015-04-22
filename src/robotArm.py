from loader import config
import dhmatrix
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class robotArm:

    def __init__(self):
        self.joint = config.joint
        self.hasChanged = True
        self.updateAllTransformer()
        self.updateAllState()

    def draw(self):
        glLineWidth(5)
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        base = None
        print "start--------------------------------------"
        for p in self.states:
            if base is not None:
                glVertex3f(base[0, 3], base[1, 3], base[2, 3])
                glVertex3f(p[0, 3], p[1, 3], p[2, 3])
                print 'line', (base[0, 3], base[1, 3], base[2, 3]), (p[0, 3], p[1, 3], p[2, 3])
            base = p
        glEnd()

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