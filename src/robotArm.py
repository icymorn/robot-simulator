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
        # glLoadIdentity()
        # glLineWidth(5)
        glColor3f(0.0, 1.0, 0.0)
        # t = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
        # glLoadMatrixd(t)
        # glBegin(GL_LINES)

        # base = None
        # for p in self.states:
        #     if base is not None:
        #         glVertex3f(base[0, 3], base[1, 3], base[2, 3])
        #         glVertex3f(p[0, 3], p[1, 3], p[2, 3])
        #         # print 'line: ', (base[0, 3], base[1, 3], base[2, 3]), (p[0, 3], p[1, 3], p[2, 3])
        #     base = p
        # glEnd()

        last = None
        quadratic = gluNewQuadric()

        for j in self.joint:
            # if j.d is not 0:
                # glColor3f(0.0, 1.0, 0.0)
            # glPushMatrix()
            #
            # glRotated(math.degrees(j.theta), 0, 0, 1)
            # glPushMatrix()
            # glutSolidSphere(0.03,10,10)
            # # gluCylinder(quadratic, 0.05, 0, j.d, 4, 4)
            # # gluCylinder(quadratic, 0.05, 0.05, j.d, 4, 4)
            # # glTranslated(0,0,j.d / 2.0)
            # # glutSolidCube(0.05)
            #
            # glPopMatrix()
            #
            glColor3f(1.0, 0.0, 0.0)
            #
            # glPopMatrix()
            # glutSolidCube(0.03)
            glPushMatrix()
            glRotated(math.degrees(j.theta), 0, 0, 1)
            glColor3f(0, 1, 0)
            if j.d < 0.02:
                gluCylinder(quadratic, 0.04, 0.04, 0.02, 10, 10)
            else:
                gluCylinder(quadratic, 0.04, 0.04, j.d, 10, 10)
            glTranslated(0, 0, j.d)

            glColor3f(1.0, 0.0, 0.0)
            # if j.alpha > 0.01:
            #     glRotatef(90, 0, 0, 1)
            # glRotatef(math.degrees(-j.alpha), 1, 0, 0)
            # if j.r < 0.02:
            #     gluCylinder(quadratic, 0.02, 0.02, 0.02, 10, 10)
            # else:
            #     gluCylinder(quadratic, 0.02, 0.02, j.r, 10, 10)
            glPopMatrix()

            # glMultMatrixd(j.iniM().transD().rotTheta().transR().rotAlpha().m.transpose())
            glMultMatrixd(j.iniM().transD().rotTheta().transR().m.transpose())

            glPushMatrix()
            glRotatef(-90, 0, 1, 0)
            gluCylinder(quadratic, 0.02, 0.02, j.r, 10, 10)
            glColor3f(1.0, 0.0, 0.0)
            glPopMatrix()

            glMultMatrixd(j.iniM().rotAlpha().m.transpose())
            # glRotated(180, 0, 0, 1)
            # glMultMatrixd(j.iniM().rotAlpha().m.I.transpose())
            # glMultMatrixd(j.transR().rotAlpha().m)
            last = j

        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glRotated(math.degrees(last.theta), 0, 0, 1)
        glColor3f(0, 1, 0)
        gluCylinder(quadratic, 0.04, 0.04, last.d, 10, 10)
        glPopMatrix()

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