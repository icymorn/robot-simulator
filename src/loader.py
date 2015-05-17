import yaml
import dhmatrix
import servo

class Config:

    def __init__(self, filename):
        stream    = file(filename, 'r')
        self.data = yaml.load(stream)

        self.realClaw = {}
        for servoData in self.data['real_robot']:
            self.realClaw[servoData['port']] = servo.Servo(servoData)

        self.joint = []
        for m in self.data['robot_arm']:
            self.joint.append(dhmatrix.DHMatrix(m['theta'], m['d'], m['r'], m['alpha'], m['transform']['scale'], m['transform']['offset'], self.realClaw[m['bind_port']]))

        self.port = self.data['backend_server']['port']
        self.realClawRotate = servo.Servo(self.data['real_claw_rotate'])
        self.realClaw = servo.Servo(self.data['real_claw'])

def main():
    config = Config('../config.yaml')

if __name__ == '__main__':
    main()
else:
    config = Config('../config.yaml')