import sys
import os.path

try:
    import OpenGL               #< Delete these two lines if the freeglut
    OpenGL.USE_FREEGLUT = True  #< library is not available to PyOpenGL;
    from OpenGL.GL import *     #  also make sure HAVE_FREEGLUT = False.
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print ''' Error: PyOpenGL not installed properly !!'''
    sys.exit()
    
try:
    from PIL import Image
    HAVE_PIL_IMAGE = True
except:
    print ''' Note: This module requires PIL to capture images'''
    HAVE_PIL_IMAGE = False

from locale import format_string

class SampleSelectObj:

    def __init__(self, argv):
        """ Constructor to initialize a Sample Selection Object
        """
        self.PROJMODE   = 0     # Projection mode (0=orthographic, 1=perspective)
        self.SELECTVXYZ = []    # Selection volume vertex coordinates array
        self.ROTXY      = []    # Rotation mouse x and y values
        self.ZYROT      = 1     # Rotation mode (0=XY, 1=ZY)
        self.XROTANG    = 0.0   # Rotation angle about X-axis
        self.YROTANG    = 0.0   # Rotation angle about Y-axis
        self.ZROTANG    = 0.0   # Rotation angle about Z-axis
        self.CAPTURE    = False # Capture image toggle switch (True/False)
        self.CAPIMGDIR  = "."   # Captured images directory
        self.EXIT_GLUT  = False # Exit GLUT main event loop flag

        
        # Timers and counters
        self.t            = 0
        self.msec_counter = 0
        self.frame_time   = 0
        self.img_count    = 0
        
        # Initialize GLUT
        glutInit(argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(400, 300)
        glutInitWindowPosition(100, 100)
        self.window = glutCreateWindow(argv[0])
        
        # Initialize SampleSelectObj display
        self.initDisplay(argv)
        
        # Register SampleSelectObj handlers with GLUT
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutMouseFunc(self.select)
        glutMotionFunc(self.motion)
        glutKeyboardFunc(self.keyboard)

    def applyRotation(self):
        """ Applies ZY or XY rotation.
        """
        if self.ZYROT :
            glRotatef(self.ZROTANG, 0.0, 0.0, 1.0)
            glRotatef(self.YROTANG, 0.0, 1.0, 0.0)
        else :
            glRotatef(self.XROTANG, 1.0, 0.0, 0.0)
            glRotatef(self.YROTANG, 0.0, 1.0, 0.0)
            
    def renderPick(self):
        """ glSelectWithCallback render callback -
              Renders cube and sphere for picking.
        """
        glPushName(0)
        self.drawCube()
        glPopName()
        glPushName(1)
        self.drawSphere()
        glPopName()
        
    def glSelectWithCallback(self, x, y, callback, \
                             xsize = 5, ysize = 5, buffer_size = 512):
        """ glSelectWithCallback(int x, int y, Callable callback, 
                                 int xsize=5, int ysize=5, int buffer_size=512)
    
            x,y         -- x and y window coordinates for the center of the 
                           pick box
            callback    -- render callback (callable Python object) taking 0 
                           arguments which performs pick-mode rendering
            xsize,ysize -- x and y dimensions of the pick box (default = 5x5)
            buffer_size -- bytes allocated for pick results buffer
    
            The function returns a tuple (possibly empty) of:
              (minimumzdepth, maximumzdepth, (name, name, name,...),...)
                minimumzdepth, maximumzdepth -- 0.0 to 1.0 corresponding to
                  depth from near to far planes of viewing volume frustum
                  If you want physical depth, multiply that by the frustum 
                  depth and add your near clipping plane.py.  This is valid only
                  for orthographic projections since depth values are non-
                  linear for perspective projectons.
                name -- the names (integers) used in calls to glPushName(int)
        """
        viewport = glGetIntegerv(GL_VIEWPORT)
        previousprojmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
        glSelectBuffer(buffer_size)
        glRenderMode(GL_SELECT)
        glInitNames()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPickMatrix(float(x), float(viewport[3] - y), xsize, ysize, viewport)
        glMultMatrixd(previousprojmatrix)
        glMatrixMode(GL_MODELVIEW)
        callback()
        glFlush()
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixd(previousprojmatrix)
        glMatrixMode(GL_MODELVIEW)
        return glRenderMode(GL_RENDER)

    def drawSelectVolume(self):
        """ Draws wire-frame select volume in the world space.
        """
        if len(self.SELECTVXYZ) == 4 or len(self.SELECTVXYZ) == 8 :
            glPushMatrix()
            self.applyRotation()
            glColor3f(1.0, 1.0, 1.0)
            glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0, 1.0, 1.0, 1.0])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
            glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
            glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 1.0, 1.0, 1.0])
            # Draw pick box
            glBegin(GL_LINE_LOOP)
            for i in [0,1,2,3] :
                glVertex3f(self.SELECTVXYZ[i][0], \
                           self.SELECTVXYZ[i][1], \
                           self.SELECTVXYZ[i][2])
            glEnd()
            if len(self.SELECTVXYZ) == 8 :
                # Draw select volume
                glBegin(GL_LINE_LOOP)
                for j in [4,5,6,7] :
                    glVertex3f(self.SELECTVXYZ[j][0], \
                               self.SELECTVXYZ[j][1], \
                               self.SELECTVXYZ[j][2])
                glEnd()
                glBegin(GL_LINES)
                for i in [0,1,2,3] :
                    j = i + 4
                    glVertex3f(self.SELECTVXYZ[i][0], \
                               self.SELECTVXYZ[i][1], \
                               self.SELECTVXYZ[i][2])
                    glVertex3f(self.SELECTVXYZ[j][0], \
                               self.SELECTVXYZ[j][1], \
                               self.SELECTVXYZ[j][2])
                glEnd()
            glPopMatrix()
    
    def getSelectVolume(self, n, mx, my):
        """ Gets the near plane.py and far plane.py world space coordinates
            of the clip volume corresponding to the pick box centered 
            about the mouse cursor coordinates in the viewport. 
        """
        # Using default x and y dimensions (5x5) of the pick box for
        # the x and y size of the select volume.
        dx = [-2.5,  2.5,  2.5, -2.5, -2.5,  2.5,  2.5, -2.5]
        dy = [-2.5, -2.5,  2.5,  2.5, -2.5, -2.5,  2.5,  2.5]
        # Using 0.01 and 0.99 for near and far z limits of the select
        # volume to prevent the end planes of the drawn select volume
        # from being clipped by the near (0.0) and far (1.0) clipping 
        # planes of the viewing volume.
        z = [0.01, 0.01, 0.01, 0.01, 0.99, 0.99, 0.99, 0.99]
        # Get viewport, projection and modelview matrices for UnProject
        viewport   = glGetIntegerv(GL_VIEWPORT) 
        projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
        glPushMatrix()
        self.applyRotation()
        mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        # Convert mouse (x,y) to viewport (vx,vy)
        print "Coordinates at mouse cursor are (%4d,%4d)" % (mx,my)
        vx = float(mx)
        vy = float(viewport[3] - my) 
        # Convert select view volume coordinates (x,y,z) to world 
        # coordinates (wx,wy,wz)
        selectvol = []
        if ( n == 4 ) :
            print "Select rectangle vertices in world coordinates:"
        elif ( n == 8 ) :
            print "Select volume vertices in world coordinates:"
        for k in range(n):
            x = vx + dx[k]
            y = vy + dy[k]
            (wx,wy,wz) = gluUnProject(x,y,z[k],mvmatrix,projmatrix,viewport)
            print " at z = %f are (%f, %f, %f)" % (z[k], wx, wy, wz)
            selectvol.append((wx, wy, wz))
        return selectvol

    def select(self, button, state, mx, my):
        """ glutMouseFunc handler -
              Performs selection or rotation processing based
              on mouse button, state and coordinates.
        """
        if ( button == GLUT_LEFT_BUTTON and state == GLUT_DOWN ):
            # Enter selection mode - set pick box
            self.SELECTVXYZ = self.getSelectVolume(4,mx,my)
            glutPostRedisplay()
        elif ( button == GLUT_LEFT_BUTTON and state == GLUT_UP ):
            # Exit selection mode - perform pick rendering
            self.SELECTVXYZ = self.getSelectVolume(8,mx,my)
            result = self.glSelectWithCallback(mx, my, self.renderPick)
            glutPostRedisplay()
            print "Objects selected - name at (near,far):"
            if result :
                i = 0
                while i < len(result):
                    near = result[i].near
                    far  = result[i].far
                    k = 0
                    while k < len(result[i].names):
                        key = result[i].names[k]
                        if  key == 0  : name = "CUBE"
                        elif key == 1 : name = "SPHERE"
                        else          : name = "UNKNOWN"            
                        print " %s at (%f, %f)" % (name,near,far)
                        k += 1
                    i += 1
            else : print '- NOTHING!'
        elif ( button == GLUT_MIDDLE_BUTTON and state == GLUT_DOWN ):
            # Enter rotation mode
            self.ROTXY.append((mx,my))
        elif ( button == GLUT_MIDDLE_BUTTON and state == GLUT_UP ):
            # Exit rotation mode
            self.ROTXY = []
     
    def motion(self, mx, my):
        """ glutMotionFunc handler -
              Sets selection SELECTVXYZ or rotation ROTXY data
              objects based on current mouse button mode.
        """
        if self.SELECTVXYZ :
            # In selection mode (left mouse button pressed)
            if len(self.SELECTVXYZ) == 4 :
                # Display pick box
                self.SELECTVXYZ = self.getSelectVolume(4,mx,my)
                self.display()
                return
        if self.ROTXY :
            # In rotation mode (middle mouse button pressed)
            viewport = glGetIntegerv(GL_VIEWPORT)
            w  = viewport[2] - viewport[0]
            h  = viewport[3] - viewport[1]
            dx = float(mx - self.ROTXY[0][0]) 
            dy = float(my - self.ROTXY[0][1])
            # Calculate rotation as 180 degrees per width and height
            self.YROTANG += 180.0*float(dx/w)
            if self.ZYROT : self.ZROTANG -= 180.0*float(dy/h)
            else          : self.XROTANG += 180.0*float(dy/h)
            self.ROTXY[0] = (mx,my)
            glutPostRedisplay()

    def keyboard(self, key, x, y):
        """ glutKeyboardFunc handler -
              Handles key presses to exit program, clear selection
              volume, set/reset image capture, change projection mode
              reset rotation angles and change rotation axis mode.
        """
        if key == '\x1b' : # esc key
            # Exit program
            if ( HAVE_FREEGLUT ) :
                glutLeaveMainLoop()
                self.EXIT_GLUT = True
                return
            else :
                sys.exit()
        if key == 'c' or key == 'C' :
            # Clear selection volume
            self.SELECTVXYZ = []
            glutPostRedisplay()
        elif key == 'i' or key == 'I' :
            # Image capture toggle
            if HAVE_PIL_IMAGE :
                self.CAPTURE = not self.CAPTURE
        elif key == 'o' or key == 'O' :
            # Orthographic projection
            if self.PROJMODE == 0 : return
            self.PROJMODE = 0
            viewport = glGetIntegerv(GL_VIEWPORT)
            self.setProjection(viewport[2],viewport[3])
            self.SELECTVXYZ = []
            glutPostRedisplay()
        elif key == 'p' or key == 'P' :
            # Perspective projection
            if self.PROJMODE == 1 : return
            self.PROJMODE = 1
            viewport = glGetIntegerv(GL_VIEWPORT)
            self.setProjection(viewport[2],viewport[3])
            self.SELECTVXYZ = []
            glutPostRedisplay()
        elif key == 'r' or key == 'R' :
            # Reset rotation angles
            self.XROTANG = 0.0
            self.YROTANG = 0.0
            self.ZROTANG = 0.0
            glutPostRedisplay()
        elif key == 'x' or key == 'X' :
            # XY rotation mode
            self.ZYROT = 0
            self.XROTANG = 0.0
            self.YROTANG = 0.0
            self.ZROTANG = 0.0
            glutPostRedisplay()
        elif key == 'z' or key == 'Z' :
            # ZY rotation mode
            self.ZYROT = 1
            self.XROTANG = 0.0
            self.YROTANG = 0.0
            self.ZROTANG = 0.0
            glutPostRedisplay()
        
    def saveImage(self):
        """ Saves image drawn in back framebuffer to a JPEG file.
        """
        if self.msec_counter == self.frame_time :
      
            # Zero millisecond counter
            self.msec_counter = 0
            
            # Get image size from current viewport size
            viewport = glGetIntegerv(GL_VIEWPORT)
            imgx     = viewport[0]
            imgy     = viewport[1]
            imgw     = viewport[2] - viewport[0]
            imgh     = viewport[3] - viewport[1]
            size     = (imgw,imgh)

            # Read color pixels from back framebuffer into data array
            glReadBuffer(GL_BACK)
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixelsub(imgx, imgy, imgw, imgh, GL_RGBA)
            assert data.shape == (imgw,imgh,4), \
                """Got back array of shape %r, expected %r""" % \
                    (data.shape, (size,4))
    
            # Get decoded image from data array
            if bool(Image.frombuffer):
                image = Image.frombuffer( "RGB", size, data,   \
                                          "raw", "RGBA", 0, -1 ) # Decoder
                                
            # Save image as a JPEG file
            scount = format_string("%04d",self.img_count)
            file   = self.CAPIMGDIR + "\img_" + scount + ".jpg"
            if bool(image):
                image.save(file,"JPEG")
            # print "time %8.3f image count = %04d " % (t,img_count)
    
            # Increment image counter
            self.img_count += 1

    def drawWorldAxes(self):
        """ Draws labeled world space reference system axes.
        """
        glPushMatrix()
        self.applyRotation()
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
  
    def drawCube(self):
        """ Draws a solid red cube.
        """
        glPushMatrix()
        self.applyRotation()
        glTranslatef(-2.0, 0.0, 0.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.6, 0.0, 0.1, 0.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glutSolidCube(1.4142)
        glPopMatrix()

    def drawSphere(self):
        """ Draws a solid blue sphere.
        """
        glPushMatrix()
        self.applyRotation()
        glRotatef(-90.0, 1.0, 0.0, 0.0) # For aesthetics, rotate GLUT sphere to
        glTranslatef(2.0, 0.0, 0.0)     # align its +Z-axis with world +Y-axis
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1, 0.0, 0.6, 0.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glutSolidSphere(1, 35, 35)
        glPopMatrix()

    def display(self):
        """ glutDisplayFunc handler -
              Draws world axes, select volume, cube and sphere
              on call and glutPostRedisplay calls.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMaterialf(GL_FRONT, GL_SHININESS, 80)
        self.drawWorldAxes()
        self.drawSelectVolume()
        self.drawCube()
        self.drawSphere()
        glFlush()
        if self.CAPTURE : self.saveImage()
        glutSwapBuffers()
  
    def setProjection(self, w, h):
        """ Sets the GL model to viewport projection transformation 
            matrix.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if w > h :
            sfac = float(w)/float(h)
            if self.PROJMODE : 
                glFrustum(-1.5*sfac, 1.5*sfac, -1.5, 1.5, 10.0, 30.0)
            else             : 
                glOrtho(-3.0*sfac, 3.0*sfac, -3.0, 3.0, 10.0, 30.0)
        else :
            sfac = float(h)/float(w)
            if self.PROJMODE : 
                glFrustum(-1.5, 1.5, -1.5*sfac, 1.5*sfac, 10.0, 30.0)
            else             : 
                glOrtho(-3.0, 3.0, -3.0*sfac, 3.0*sfac, 10.0, 30.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
  
    def reshape(self, w, h):
        """ glutReshapeFunc handler -
              Redisplays graphics context when window viewport 
              is reshaped.
        """
        glViewport(0, 0, w, h)
        self.setProjection(w, h)
        glutPostRedisplay()
  
    def setBasicLighting(self):
        """ Sets basic GL lighting parameters for a white 
            flood type light.
        """
        light_position = [0.0, 3.0, 3.0, 0.0]
        white_light    = [1.0, 1.0, 1.0, 1.0]
        lmodel_ambient = [0.2, 0.2, 0.2, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, white_light)
        glLightfv(GL_LIGHT0, GL_SPECULAR, white_light)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def initDisplay(self, argv):
        """ Initializes the GL projection mode, display,
            shading, lighting and depth test.
        """
        if argv and len(argv) > 1 : 
            if str.upper(argv[1]) == "P"   : self.PROJMODE = 1
            elif str.upper(argv[1]) == "O" : self.PROJMODE = 0
        if argv and len(argv) > 2 :
            if os.path.isdir(argv[2]) : self.CAPIMGDIR = argv[2]
            else                      : self.CAPIMGDIR = "."
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_FLAT)
        self.setBasicLighting()
        glEnable(GL_DEPTH_TEST)

if __name__ == '__main__':
    """ Main routine.
    """
    # Create and initialize a Sample Selection Object
    ssObj = SampleSelectObj(sys.argv)

    # Enter GLUT main processing loop
    if HAVE_FRE`EGLUT :
        while ( ssObj.EXIT_GLUT == False ) :
            glutMainLoopEvent()
            if ( glutGetWindow() != ssObj.window ) :
                ssObj.EXIT_GLUT = True
        if ( glutGetWindow() == ssObj.window ) : 
            glutDestroyWindow(ssObj.window)
    else :
        glutMainLoop()