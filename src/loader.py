import yaml
import dhmatrix

class Config:

    def __init__(self, filename):
        stream    = file(filename, 'r')
        self.data = yaml.load(stream)
        self.joint = []
        for m in self.data['robot_arm']:
            self.joint.append(dhmatrix.DHMatrix(m['theta'], m['d'], m['r'], m['alpha'], m['transform']['scale'], m['transform']['offset']))
        self.port = self.data['backend_server']['port']

def main():
    config = Config('../config.yaml')

if __name__ == '__main__':
    main()
else:
    config = Config('../config.yaml')