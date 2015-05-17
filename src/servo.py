import serial

class Servo:

    def __init__(self, servo):
        self.port = servo['port']
        self.start = servo['start']
        self.transform = servo['transform']
        self.scale = self.transform['scale']
        self.offset = self.transform['offset']
        self.max = self.transform['max']
        self.min = self.transform['min']

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

    def _send(self, port, pos, time = 100):
        if self.ser is None:
            print "#%dp%dt%d\r\n" % (port, int(pos), time)
        else:
            self.ser.write("#%dp%dt%d\r\n" % (port, int(pos), time))

    def reset(self):
        self._send(13, 1500)

    def open(self):
        command = self.claw.getCommand(50)
        self.sendString(command)

    def close(self):
        command = self.claw.getCommand(10)
        self.sendString(command)

    def rotate(self, value):
        command = self.clawRotate.getCommand(value)
        self.sendString(command)

    def sendString(self, command):
        if self.ser is None:
            print "sending command:", command[:-3]
        else:
            self.ser.write(command)

    def sendAngles(self, angles):
        for (i, angle) in enumerate(angles):
            self.sendString(self.arm.joint[i].bindPort.getCommand(angle))

if __name__ == '__main__':
    from robotArm import robotArm
    import time
    arm = robotArm()
    # params = {"port": 11, "start": 1000, "transform": {"scale": 1, "offset": 0, "max": 2000, "min": 1000}}
    servoServer = ServoServer(arm)
    # servoServer.rotate(-60)
    angles = arm.getCurrentAngles()
    angles[3] = 100
    angles[1] = 100
    arm.slowTo(angles, servoServer.sendAngles, True)
    time.sleep(40)
    # servo = Servo(params)
    # print servo.getCommand(50)