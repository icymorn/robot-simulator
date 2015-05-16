import serial
from robotArm import robotArm

class Servo:
    def __init__(self):
        self.ser = serial.Serial('COM3', 115200)

    def _send(self, port, pos, time = 100):
        self.ser.write("#%dp%dt%d\r\n" % (port, pos, time))

    def reset(self):
        self._send(13, 1500)

if __name__ == '__main__':
    servo = Servo()
    servo.reset()