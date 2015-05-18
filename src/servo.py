import serial
import ik
import time

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

    def getCommand(self, value, time = 100):
        return "#{0}p{1}t{2}\r\n".format(self.port, self.trans(value), time)

    def trans(self, value):
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
            self.ser = serial.Serial('COM3', 115200, timeout = 2)
        except Exception:
            print "Cannot establish connection to serial port, using the std instead"
            self.ser = None
        self.reset()

    def reset(self):
        self.hand(self.claw.defaultValue())
        self.rotate(self.clawRotate.defaultValue())

        angles = [joint.bindPort.defaultValue() for joint in self.arm.joint]
        for (i, angle) in enumerate(angles):
            self.arm.joint[i].theta = angle
            # print self.arm.joint[i].bindPort.getCommand(angle, 3000)
            self.sendString(self.arm.joint[i].bindPort.getCommand(angle, 3000))
        # time.sleep(3)

    def _send(self, port, pos, time = 100):
        if self.ser is None:
            print "#%dp%dt%d\r\n" % (port, int(pos), time)
        else:
            self.ser.write("#%dp%dt%d\r\n" % (port, int(pos), time))

    def open(self):
        command = self.claw.getCommand(80, 1000)
        self.sendString(command)
        time.sleep(1)

    def close(self):
        command = self.claw.getCommand(10, 1000)
        self.sendString(command)
        time.sleep(1)

    def hand(self, value):
        command = self.claw.getCommand(value, 1000)
        self.sendString(command)
        time.sleep(1)

    def rotate(self, value):
        command = self.clawRotate.getCommand(value, 1000)
        self.sendString(command)
        time.sleep(1)

    def moveTo(self, x, y, r = None):
        angles = self.arm.getCurrentAngles()
        if r is None:
            r = angles[0]
        angles[0] = r
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
            self.ser.write(command)

    def sendAngles(self, angles):
        for (i, angle) in enumerate(angles):
            self.sendString(self.arm.joint[i].bindPort.getCommand(angle))
        # time.sleep(3)

if __name__ == '__main__':
    from robotArm import robotArm
    import time
    arm = robotArm()
    # params = {"port": 11, "start": 1000, "transform": {"scale": 1, "offset": 0, "max": 2000, "min": 1000}}
    servoServer = ServoServer(arm)
    # servoServer.rotate(-60)
    # angles = arm.getCurrentAngles()
    # angles[3] = 100
    # angles[1] = 100
    # arm.slowTo(angles, servoServer.sendAngles, True)
    # servoServer.open()
    # servoServer.close()
    # servoServer.open()
    print "move to: 0.1, 0.1"
    servoServer.moveTo(0.1, 0.1)
    time.sleep(5)
    # servoServer.rotate(60)
    # servoServer.rotate(-30)
    # servoServer.rotate(-60)
    # servo = Servo(params)
    # print servo.getCommand(50)