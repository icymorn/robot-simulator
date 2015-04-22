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
        glPushMatrix()
        # glLoadIdentity()
        # glLineWidth(5)
        glColor3f(0.0, 1.0, 0.0)
        # t = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
        # glLoadMatrixd(t)
        glBegin(GL_LINES)

        base = None
        for p in self.states:
            if base is not None:
                glVertex3f(base[0, 3], base[1, 3], base[2, 3])
                glVertex3f(p[0, 3], p[1, 3], p[2, 3])
                # print 'line: ', (base[0, 3], base[1, 3], base[2, 3]), (p[0, 3], p[1, 3], p[2, 3])
            base = p
        glEnd()

        # for p in self.states:
        #     glutSolidCube(0.03)
        #     glMultMatrixf(p)
        # glEnd()

        # base = None
        for j in self.joint:
            if j.d is not 0:
                # glColor3f(0.0, 1.0, 0.0)
                glPushMatrix()

                glRotated(j.theta, 0, 0, 1)
                glPushMatrix()
                glutSolidSphere(0.03,10,10)
                glPopMatrix()

                glPushMatrix()
                glTranslated(0,0,j.d / 2.0)
                glutSolidCube(0.05)
                glPopMatrix()

                glColor3f(1.0, 0.0, 0.0)

                glPopMatrix()
            # glutSolidCube(0.03)
            glMultMatrixd(j.transform().transpose())
            # data = glGetFloatv(GL_MODELVIEW)
            # print j.transform()
            # a = (GLfloat * 16)()
            # mvm = glGetFloatv(GL_VIEWPORT, a)
            # print list(a)

            if j.r is not 0:
                glPushMatrix()
                glTranslated(-j.r, 0, 0)
                glutSolidSphere(0.03, 10, 10)
                glPopMatrix()
                #
                # glPushMatrix()
                # glTranslated(-j.r/2.0, 0, 0)
                # glutSolidCube(0.03)
                # glPopMatrix()
            # glVertex3f(base[0, 3], base[1, 3], base[2, 3])
            # glVertex3f(p[0, 3], p[1, 3], p[2, 3])
        glPopMatrix()

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