from loader import config
import dhmatrix
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from animate import AnimateThread

class robotArm:

    def __init__(self):
        self.joint = config.joint
        self.claw  = config.realClaw
        self.clawRotate = config.realClawRotate
        self.hasChanged = True
        self.animation = None

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

    def getCurrentAngles(self):
        return [angle.theta for angle in self.joint]

    def slowTo(self, jointAngles, callback, needParams = True):
        if self.animation is not None and self.animation.isRunning:
            self.animation.cancel()
        startAngle = self.getCurrentAngles()
        endAngle   = jointAngles
        animate    = AnimateThread(startAngle, endAngle, 3)
        animate.setCallback(callback, needParams)
        animate.setDaemon(True)
        self.animation = animate
        animate.start()
