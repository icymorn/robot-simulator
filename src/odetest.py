# a ball on the ground, which can be controlled to roll
# ed paradis, jan 2007

# some code borrowed from http://pyode.sourceforge.net/tutorials/tutorial3.html

import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode

############################### fucntions ##################################

def normalize(V):
    len = length(V)
    return (V[0] / len, V[1] / len, V[2] / len)

def cross(U,V):
    return (-U[2]*V[1]+U[1]*V[2], U[2]*V[0]-U[0]*V[2], -U[1]*V[0]+U[0]*V[1])

def length (vec):
    return sqrt (vec[0]**2 + vec[1]**2 + vec[2]**2)

# return the angle between two 3d vectors (acos of A dot B)
def angle3d( A, B):
    return acos( (A[0]*B[0] + A[1]*B[1] + A[2]*B[2]) / (length(A)*length(B)))

# return a vector subtration
def sub3d( A, B):
    x = A[0] - B[0]
    y = A[1] - B[1]
    z = A[2] - B[2]
    return (x,y,z) 

def drawText(stringoftext, x, y):
    glPushMatrix()
    c = 0
    # render something to the screen
    glRasterPos2f(x,y)
    for c in stringoftext:
        glutBitmapCharacter( GLUT_BITMAP_HELVETICA_18, ord(c) )
    glPopMatrix()

# prepare_GL
def prepare_GL():
    """Prepare drawing.
    """

    global target

    # Viewport
    glViewport(0,0,640,480)

    # Initialize
    glClearColor(0.8,0.8,0.9,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_FLAT)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective (45,1.3333,0.2,20)

    # Initialize ModelView matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Light source
    glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
    glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
    glEnable(GL_LIGHT0)

    # View transformation
    gluLookAt (2.4, 3.6, 4.8,  target[0], target[1], target[2],   0, 1, 0)

# Collision callback
def near_callback(args, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.
    """

    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.8)    # bouncyness
        c.setMu(800)       # friction for both surfaces
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())


# create a ball
def create_ball(world, space, density, radius):
    """create a ball body and its corresponding geom."""

    #create the body  (the physical volume to simulate)
    body = ode.Body(world)
    M = ode.Mass()
    M.setSphere( density, radius)
    body.setMass(M)

    # set parameters for drawing the body
    body.shape = "ball"
    body.radius = radius

    # create a sphere geom for collision detection
    geom = ode.GeomSphere(space, radius=body.radius)
    geom.setBody(body)

    return body

# create a box
def create_box(world, space, density, lx, ly, lz):
    """Create a box body and its corresponding geom."""

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setBox(density, lx, ly, lz)
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "box"
    body.boxsize = (lx, ly, lz)

    # Create a box geom for collision detection
    geom = ode.GeomBox(space, lengths=body.boxsize)
    geom.setBody(body)

    return body


# insert objects into scene. called once at startup on the first frame
def insert_objects():
    """insert an object into the scene"""

    global bodies, j1

    # first we place the 'ball'
    body = create_ball(world, space, 1000, 0.30)
    body.setPosition( (0,1.0,0) )    # in the center, above the floor
    bodies.append(body)

    # then we place the 'stick'
    body = create_box(world, space, 1000, 0.1, 1.0, 0.1 )
    body.setPosition( (0,2,0) )
    bodies.append(body)

    j1.attach(bodies[0], bodies[1])
    j1.setAxis1( (1,0,0) )
    j1.setAxis2( (0,0,1) )
    j1.setParam( ode.ParamFMax, 400)
    j1.setParam( ode.ParamFMax2, 400)

    j1.setAnchor( (0,1,0) )

    # now we place some sticks for the ball to run into
    body = create_box( world, space, 1000, 0.1, 1.0, 0.1)
    body.setPosition( (-0.1,.5,2) )
    bodies.append(body)
    body = create_box( world, space, 1000, 0.1, 1.0, 0.1)
    body.setPosition( (2, .5, 0.1) )
    bodies.append(body)

    # and some walls!
    body = create_box( world, space, 10000, 10, 0.5, 0.1)
    body.setPosition( (0, .25, 5))
    bodies.append(body)
    body = create_box( world, space, 10000, 10, 0.5, 0.1)
    body.setPosition( (0, .25, -5))
    bodies.append(body)
    body = create_box( world, space, 10000, 0.1, 0.5, 9.9)
    body.setPosition( (-5, .25, 0))
    bodies.append(body)
    body = create_box( world, space, 10000, 0.1, 0.5, 9.9)
    body.setPosition( (5, .25, 0))
    bodies.append(body)


    
# draw a body. currently does balls and boxes.  I would like to also somehow
#  draw the floor
def draw_body(body):
    """draw an ODE body."""

    x,y,z = body.getPosition()
    R = body.getRotation()
    rot = [R[0], R[3], R[6], 0.,
           R[1], R[4], R[7], 0.,
           R[2], R[5], R[8], 0.,
           x, y, z, 1.0]
    glPushMatrix()
    glMultMatrixd(rot)
    if body.shape=="box":
        sx,sy,sz = body.boxsize
        glScale(sx, sy, sz)
        glutSolidCube(1)
    elif body.shape=="ball":
        rad = body.radius
        glutSolidSphere( rad, 24, 24)
    glPopMatrix()

# draw a line given two points and color
def draw_line( start, stop) :
    glPushMatrix()
    glBegin( GL_LINES)
    glVertex3f( start[0], start[1], start[2] )
    glVertex3f( stop[0], stop[1], stop[2] )
    glEnd()
    glPopMatrix()

def draw_triangle( A, B, C):
    glPushMatrix()
    glBegin( GL_TRIANGLES)
    glVertex3f( A[0], A[1], A[2])
    glVertex3f( B[0], B[1], B[2])
    glVertex3f( C[0], C[1], C[2])
    glEnd()
    glPopMatrix()

# draw a grid of lines at the origin
def draw_grid():
    for a in range(-5, 6):
        draw_line( (a, 0, -5), (a, 0, 5))
        draw_line( (-5, 0, a), (5, 0, a))
   
############################### end of functions ###########################

#initialize GLUT
glutInit ([])

#open a window
glutInitDisplayMode ( GLUT_RGB | GLUT_DOUBLE )

x = 0
y = 0
width = 640
height = 480
glutInitWindowPosition(x,y)
glutInitWindowSize(width, height)
glutCreateWindow ("ball and stick simulator")

# create world object (the dynamics world)
world = ode.World()
world.setGravity( (0, -9.81, 0) )
world.setERP(0.8)   # error reduction parameter
world.setCFM(1E-5)  # constraint force mixing

# create a space object ( a collision space)
space = ode.Space()

# create a plane.py geom for the floor (infinite plane.py)
floor = ode.GeomPlane(space, (0,1,0), 0)

# a list with ODE bodies ( a body is a rigid body )
bodies = []

# a joint group for the contact joints that are generated whenever two bodies
#  collide
contactgroup = ode.JointGroup()

# crreate a joint between the ball and the stick
j1 = ode.UniversalJoint(world)

# simulation loop variables
fps = 50
dt = 1.0 / fps
running = True
lasttime = time.time()
state = 0
counter = 0
theta2 = 0
e1 = 0
e2 = 0
e3 = 0
P_const = 40.0
I_const = 0.0 
D_const = 0.0

I_state = 0
D_state = 0
I_state2 = 0
D_state2 = 0
I_state_max = 30
I_state_min = -30

command_tilt = (0,1,0)

############################## glut call backs #############################

# keyboard callback for glut
def _keyfunc (c,x,y):
    sys.exit(0)

# hook the keyboard callback
glutKeyboardFunc (_keyfunc)

# draw callback for glut
def _drawfunc():
    global theta2, e1,e2, e3, phi, theta, rho, angle1, angle2, command_tilt, target

    target = bodies[0].getPosition()

    # draw the scene
    prepare_GL()

    # draw the grid lines
    draw_grid()
    
    # draw all the bodies
    for b in bodies:
        draw_body(b)

    # we construct the normal for each axis plane.py and the
    #  vector from the center of the ball to the center of the stick
    axis_of_balance = sub3d( bodies[1].getPosition(), bodies[0].getPosition())
    normal1 = cross( j1.getAxis2(), axis_of_balance)
    normal2 = cross( normal1, axis_of_balance)
    
    # the normal for the floor is simply unit vector in y direction
    #floor_normal = (0,1,0)
    floor_normal = normalize(command_tilt)

    # now we find the dihedral angles between the floor and the axis planes
    #  but because this uses acos, we loose signedness
    angle1 = angle3d( normal1, floor_normal)    # between 0 and pi radians
    angle2 = angle3d( normal2, floor_normal)    #  (eqv to 0 to 180 degrees)
 
    #inwardsness1 = 1 - length(sub3d(j1.getAxis2(), normal1) )

    # we want the axis to maintain a 90 degree difference betwen the 
    #  planes of axis and the floor 
    angle1 = angle1 - (3.14/2)
    angle2 = angle2 - (3.14/2)

    #print "angle1: "+str(round(180/3.14*angle1,2))+" angle2: "+str(round(180/3.14*angle2,2))
    #print "<",
    #for x in axis_of_balance:
    #    print round(x,2),
    #print ")"

    # visualization of normals
    v0 = bodies[0].getPosition()
    v1 = sub3d( v0, normal1 )
    v2 = sub3d( v0, normal2)
    v3 = sub3d( v0, j1.getAxis1())
    v4 = sub3d( v0, j1.getAxis2())
    draw_triangle( v0, v1, v2)
    draw_line( v0, v1)
    draw_line( v0, v2)
    draw_line( v0, v3)
    draw_line( v0, v4)
    
    #draw_line( (0,0,0), j1.getAxis1() )

    #draw_line( v0, subcross(normal1, normal2)

    # calculate the angle that the stick is leaning from vertical
    #T = bodies[0].getPosition() # T is sphere
    #Q = bodies[1].getPosition() # Q is stick
    #V = ( T[0], 4, T[2] )   # point above the sphere
    #vector_of_stick = sub3d( T, Q)
    #vertical_vector = sub3d( T, V)
    #angle = 180 / 3.14 * angle3d( vector_of_stick, vertical_vector)

    #drawText( "angle1: "+str(round(angle1,3)), -2,2.5 )
    #drawText( "angle2: "+str(round(angle2,3)), -2,2.2 )
    #drawText( "phi: "+str(round(phi,3)), -1.5,1.2 )

    #i = 0
    #for x in bodies[0].getRotation():
    #    if (i%3 == 0):
    #        print
    #    print str(round(x,2)),
    #    i=i+1
    #print

    # the stick's rotation matrix
    #R = bodies[1].getRotation()

    # convert to euler angles (3-1-3, x-convention)
    #phi = atan2(R[6],R[7])  # which way the stick is pointing
    #theta = acos(R[8])      # 
    #rho = -atan2(R[2],R[5]) #
    #print "                                ",round(180 / 3.14 * phi,2), round(180 / 3.14 * theta,2) , round(180/3.14*rho,2)
    
    #if (rho < 0):
    #    theta = theta * -1

    #drawText( "phi: "+str(round(phi,3)), -2,2.2 )
    #drawText( "theta: "+str(round(theta,3)), -2,2 )
    #drawText( "rho: "+str(round(rho,3)), -2,1.7)

    #theta2 = acos( 0.5 * ( R[0] + R[4] + R[8] - 1))
    #denom = 2 * sin(theta2)
    #if (denom != 0):
    #    e1 = (R[5] - R[7]) / denom 
    #    e2 = (R[6] - R[2]) / denom
    #    e3 = (R[1] - R[3]) / denom
    #print round( 180 / 3.14 * theta2, 2), round(e1, 2), round(e2,2), round(e3,2)

    glutSwapBuffers ()

# hook the draw callback
glutDisplayFunc (_drawfunc)

################################### main loop ##############################

# idle callback for glut
def _idlefunc():
    global counter, state, lasttime, P_const, D_const, I_const, I_state, D_state, I_state_max, I_state_min, I_state2, D_state2,  angle1, angle2, command_tilt

    vel1 = 0
    vel2 = 0

    t = dt - (time.time() - lasttime)
    if (t>0):
        time.sleep(t)

    counter += 1


    # state machine for behavior
    if state>1:
        # balance the stick! 
        fca = -angle2
        #if (e1 < 0):
        #    fca = (abs(fca))
        #else:
        #    fca = -1* abs(fca)
        
        P_term = fca * P_const
        D_term = D_const * ( fca - D_state)
        D_state = fca
        I_state = I_state + fca
        if (I_state > I_state_max):
            I_state = I_state_max
        elif (I_state < I_state_min):
            I_state = I_state_min
        I_term = I_state * I_const

        vel1 = P_term + D_term + I_term

        #print "P: "+str(round(P_term,2))+" I: "+str(round(I_term,2))+" D: "+str(round(D_term,2))

        j1.setParam(ode.ParamVel, vel1) 

        # The other axis
        sca = angle1

        #if (e3 < 0):
        #    sca = -1 * (abs(sca))
        #else:
        #    sca = 1 * abs(sca)
        
        P_term = sca * P_const
        D_term = D_const * ( sca - D_state2)
        D_state2 = sca
        I_state2 = I_state2 + sca
        if (I_state2 > I_state_max):
            I_state2 = I_state_max
        elif (I_state2 < I_state_min):
            I_state2 = I_state_min
        I_term = I_state2 * I_const

        vel2 = P_term + D_term + I_term

        #print "                                   P: "+str(round(P_term,2))+" I: "+str(round(I_term,2))+" D: "+str(round(D_term,2))

        j1.setParam(ode.ParamVel2, vel2) 

        if state==2:
            command_tilt = (0.2,1,0)
            if counter > 100:
                counter = 0
                state = 3
        elif state==3:
            command_tilt = (-0.2,1,0)
            if counter > 200:
                counter = 0
                state = 2
        print state

    elif state==1:
        # just let the stick fall over (just a little)
        if (counter > 20):
            state = 2
            counter = 0
        j1.setParam(ode.ParamVel, -2)
        #j1.setParam(ode.ParamVel2, 2)

    elif state==0:
        # ...and on the null state, he populated the world
        insert_objects()
        state=1
    
    glutPostRedisplay()

    # simulate n collisions per ???
    n = 2

    for i in range(n):
        # detect collisions and create contact joints
        space.collide((world,contactgroup), near_callback)

        # simulation step
        world.step(dt/n)

        # remove all contact joints 
        contactgroup.empty()

    lasttime = time.time()

# hook the glut idle callback
glutIdleFunc (_idlefunc)

#enter the glut main loop (from which we exit via the keyboard callback)
glutMainLoop()
