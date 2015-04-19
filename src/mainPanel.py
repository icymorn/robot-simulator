from wx import glcanvas
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import wx


class RobotView(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self, 1, flag = wx.EXPAND)
        parent.SetSizer(hBox)
        self.init = False
        self.context = glcanvas.GLContext(self)
        
        # initial mouse position
        self.size = None
        self.resizeNeeded = True
        self.cameraMoved = True
        # self.projection = Projection(30.0, 0.1, 20)

        self.SELECTVXYZ = []    # Selection volume vertex coordinates array
        self.ROTXY      = []    # Rotation mouse x and y values
        self.ZYROT      = 1     # Rotation mode (0=XY, 1=ZY)
        self.XROTANG    = 0.0   # Rotation angle about X-axis
        self.YROTANG    = 0.0   # Rotation angle about Y-axis
        self.ZROTANG    = 0.0   # Rotation angle about Z-axis

        self.cameraDistance = 10
        self.cameraHorizonalAngle = 0.0
        self.cameraVerticalAngle = 0.0
        self.originalPoint = [0.0, 0.0, 0.0]

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)

    def applyRotation(self):
        if self.ZYROT :
            glRotatef(self.ZROTANG, 0.0, 0.0, 1.0)
            glRotatef(self.YROTANG, 0.0, 1.0, 0.0)
        else :
            glRotatef(self.XROTANG, 1.0, 0.0, 0.0)
            glRotatef(self.YROTANG, 0.0, 1.0, 0.0)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        self.resizeNeeded = True
        # wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def OnWheel(self, event):
        delta = event.GetWheelRotation()
        if delta > 0:
            self.cameraDistance += 2
        else:
            self.cameraDistance -= 2
        self.cameraMoved = True
        self.Refresh(False)

    def moveCamera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # gluLookAt(
        #     math.cos(self.cameraVerticalAngle) * math.cos(self.cameraHorizonalAngle) * self.cameraDistance,
        #     math.sin(self.cameraVerticalAngle) * self.cameraDistance,
        #     math.cos(self.cameraVerticalAngle) * math.sin(self.cameraHorizonalAngle) * self.cameraDistance,
        #     0,
        #     0,
        #     0,
        #     0.0, 10.0, 0.0)
        gluLookAt(
            self.originalPoint[0] + math.cos(self.cameraVerticalAngle) * math.cos(self.cameraHorizonalAngle) * self.cameraDistance,
            self.originalPoint[1] + math.sin(self.cameraVerticalAngle) * self.cameraDistance,
            self.originalPoint[2] - math.cos(self.cameraVerticalAngle) * math.sin(self.cameraHorizonalAngle) * self.cameraDistance,
            self.originalPoint[0],
            self.originalPoint[1],
            self.originalPoint[2],
            0.0, 10.0, 0.0)

    def DoSetViewport(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        size = self.size = self.GetClientSize()
        gluPerspective(10., size.width / float(size.height), 1., 100.)
        glViewport(0, 0, size.width, size.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.moveCamera()

    def OnPaint(self, event):
        # dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        elif self.resizeNeeded:
            self.DoSetViewport()
            self.resizeNeeded = False
        if self.cameraMoved:
            self.moveCamera()
            self.cameraMoved = False
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.ROTXY.append(evt.GetPosition())
        # self.x, self.y = self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()
        self.ROTXY = []

    def OnMouseMotion(self, evt):
    #     if evt.Dragging() and evt.LeftIsDown():
    #         self.lastx, self.lasty = self.x, self.y
    #         self.x, self.y = evt.GetPosition()
    #         self.Refresh(False)
        if self.ROTXY and evt.LeftIsDown():
            viewport = glGetIntegerv(GL_VIEWPORT)
            mx, my = evt.GetPosition()
            w  = viewport[2] - viewport[0]
            h  = viewport[3] - viewport[1]
            dx = float(mx - self.ROTXY[0][0])
            dy = float(my - self.ROTXY[0][1])
            # Calculate rotation as 180 degrees per width and height
            self.cameraHorizonalAngle -= dx * 0.01
            self.cameraVerticalAngle += dy * 0.01
            self.ROTXY[0] = (mx, my)
            self.cameraMoved = True
            self.Refresh(False)
            # glutPostRedisplay()

    def InitGL( self ):
        glMatrixMode(GL_PROJECTION)
        # camera frustrum setup
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)
        glMaterial(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterial(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterial(GL_FRONT, GL_SPECULAR, [1.0, 0.0, 1.0, 1.0])
        glMaterial(GL_FRONT, GL_SHININESS, 50.0)
        glLight(GL_LIGHT0, GL_AMBIENT, [0.0, 1.0, 0.0, 1.0])
        glLight(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLight(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLight(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # position viewer
        glMatrixMode(GL_MODELVIEW)
        # position viewer
        glTranslatef(0.0, 0.0, -2.0)
        #
        glutInit()
        # glutInit(sys.argv)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawWorldAxes()
        self.drawCube()
        self.SwapBuffers()

    def drawCube(self):
        glPushMatrix()
        # self.applyRotation()
        glTranslatef(-2.0, 0.0, 0.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.6, 0.0, 0.1, 0.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glutSolidCube(1.4142)
        glPopMatrix()

    def drawWorldAxes(self):
        glPushMatrix()
        # self.applyRotation()
        glColor3f(0.0, 1.0, 0.0)
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 1.0, 0.0, 1.0])
        glBegin(GL_LINES)
        glVertex3f( 0.0, 0.0, 0.0)
        glVertex3f( 0.8, 0.0, 0.0) # X-axis
        glVertex3f( 0.0, 0.0, 0.0)
        glVertex3f( 0.0, 0.8, 0.0) # Y-axis
        glVertex3f( 0.0, 0.0, 0.0)
        glVertex3f( 0.0, 0.0, 0.8) # Z-axis
        glEnd()
        glBegin(GL_LINE_STRIP) # letter Z
        glVertex3f(-0.1, 0.1, 1.0)
        glVertex3f( 0.1, 0.1, 1.0)
        glVertex3f(-0.1,-0.1, 1.0)
        glVertex3f( 0.1,-0.1, 1.0)
        glEnd()
        glRotatef(-self.YROTANG, 0.0, 1.0, 0.0)
        glBegin(GL_LINE_STRIP) # letter Y
        glVertex3f(-0.1, 1.2, 0.0)
        glVertex3f( 0.0, 1.1, 0.0)
        glVertex3f( 0.0, 1.0, 0.0)
        glVertex3f( 0.0, 1.1, 0.0)
        glVertex3f( 0.1, 1.2, 0.0)
        glEnd()
        glPopMatrix()

if __name__ == '__main__':
    app = wx.App()
    parent = wx.Frame(None, title="hi", size=(800, 600))
    frame = RobotView(parent)
    parent.Show()
    app.MainLoop()