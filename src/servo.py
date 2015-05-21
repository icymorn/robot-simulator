import serial
import random
from math import pi

class Servo:

    def __init__(self, servo):
        self.port = servo['port']
        self.start = servo['start']
        self.transform = servo['transform']
        self.scale = self.transform['scale']
        self.offset = self.transform['offset']
        self.max = self.transform['max']
        self.min = self.transform['min']

    def defaultValue(self):
        return self.getAngle(self.start)

    def getCommand(self, value, during = 150):
        return "#{0}p{1}t{2}\r\n".format(self.port, self.trans(value), during)

    def trans(self, value):
        value = value * 180 / pi
        newValue = int(value * self.scale + self.offset)
        if newValue > self.max:
            return self.max
        elif newValue < self.min:
            return self.min
        else:
            return newValue

    def getAngle(self, value):
        return (value - self.offset) / self.scale

    def resetCommand(self):
        return self.getCommand(self.trans(self.start), 1500)

class ServoServer:
    def __init__(self, arm):
        self.arm = arm
        self.claw = arm.claw
        self.clawRotate = arm.clawRotate
        try:
            self.ser = serial.Serial('COM4', 115200, timeout = 2)
        except Exception:
            print "Cannot establish connection to serial port, using the std instead"
            self.ser = None
        self.reset()

    def reset(self):
        self.hand(self.claw.defaultValue())
        self.rotate(self.clawRotate.defaultValue())

        angles = [joint.bindPort.defaultValue() * pi / 180 for joint in self.arm.joint]
        for (i, angle) in enumerate(angles):
            self.arm.joint[i].theta = angle
            # print self.arm.joint[i].bindPort.getCommand(angle, 3000)
            self.sendString(self.arm.joint[i].bindPort.getCommand(angle, 3000))
            time.sleep(1)

    def _send(self, port, pos, time = 150):
        if self.ser is None:
            print "#%dp%dt%d\r\n" % (port, int(pos), time)
        else:
            self.ser.write("#%dp%dt%d\r\n" % (port, int(pos), time))

    def open(self):
        command = self.claw.getCommand(100 / 180.0 * pi, 1000)
        self.sendString(command)
        time.sleep(1)

    def close(self):
        command = self.claw.getCommand(30 / 180.0 * pi, 1000)
        self.sendString(command)
        time.sleep(1)

    def hand(self, value):
        command = self.claw.getCommand(value / 180.0 * pi, 1000)
        self.sendString(command)
        time.sleep(1)

    def setBaseRotate(self, value):
        angles = self.arm.getCurrentAngles()
        print angles
        angles[0] = value * pi / 180
        print angles
        arm.slowTo(angles, self.sendAngles)
        time.sleep(3)
        print angles

    def rotate(self, value):
        command = self.clawRotate.getCommand(value * pi / 180 , 1000)
        self.sendString(command)
        time.sleep(1)

    def moveTo(self, x, y, r = None):
        import ik
        angles = self.arm.getCurrentAngles()
        if r is not None:
            angles[0] = r * pi / 180
        thetas = ik.ik(x, y)
        theta1 = thetas[0]
        theta2 = thetas[1]
        theta3 = thetas[2]
        angles[1] = theta1
        angles[2] = theta2
        angles[3] = theta3
        arm.slowTo(angles, self.sendAngles)
        time.sleep(3)

    def sendString(self, command):
        if self.ser is None:
            print "sending command:", command[:-2]
        else:
            print "sending command:", command[:-2]
            self.ser.write(command)

    def sendAngles(self, angles):
        for (i, angle) in enumerate(angles):
            print (i, angle)
            self.sendString(self.arm.joint[i].bindPort.getCommand(angle))
        # time.sleep(3)

if __name__ == '__main__':
    from robotArm import robotArm
    import time
    arm = robotArm()
    servoServer = ServoServer(arm)
    rotatelist = [-90, -45, 0, 45, 90]
    servoServer.moveTo(0.13, 0.12)
    i = random.randint(0, 4)
    servoServer.rotate(rotatelist[i])
    servoServer.open()
    servoServer.moveTo(0.16, 0.08)
    servoServer.close()
    servoServer.moveTo(0.13, 0.12)
    servoServer.open()
    time.sleep(3)
    print "================ reset"
    servoServer.reset()
    time.sleep(10)