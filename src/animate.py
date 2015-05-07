import time
import threading
from loader import config

class AnimateThread(threading.Thread):
    
    def __init__(self, startAngles, endAngles, during):
        super(AnimateThread, self).__init__()
        self.startAngles  = startAngles
        self.endAngles    = endAngles
        self.during       = during
        self.startAt      = time.time()
        self.currentAngle = startAngles[:]
        length = len(startAngles)
        self.diffAngle    = [(endAngles[i] - startAngles[i]) for i in range(length)]
        self.setCallback(self.defaultCallback)
        self.isRunning    = True

    def setCallback(self, callback):
        self.callback = callback

    def defaultCallback(self):
        print(self.currentAngle)

    def cancel(self):
        self.isRunning = False

    def run(self):
        while self.isRunning:
            currentTimeDiff = time.time() - self.startAt
            progress = currentTimeDiff / self.during
            if progress >= 1.0:
                self.isRunning = False
                progress = 1.0

            i = 0
            for angle in self.startAngles:
                self.currentAngle[i] = angle + self.diffAngle[i] * progress
                config.joint[i].setTheta(self.currentAngle[i])
                i += 1

            self.callback()
            time.sleep(0.1)

if __name__ == '__main__':
    animate = AnimateThread([5, 10], [15, 5], 2)
    animate.start()