import time
import threading

class AnimateThread(threading.Thread):
    
    def __init__(self, startAngles, endAngles, during):
        super(AnimateThread, self).__init__()
        self.startAngles  = startAngles
        self.endAngles    = endAngles
        self.during       = during
        self.startAt      = time.time()
        self.currentAngle = startAngles[:]
        self.diffAngle    = []

        i = 0
        for angle in self.startAngles:
            self.currentAngle[i] = angle - self.endAngles[i]
            i += 1
        self.setCallback(self.defaultCallback)
        self.isRunning    = True

    def setCallback(self, callback):
        self.callback = callback

    def defaultCallback(self, params):
        print(params)

    def run(self):
        while self.isRunning:
            i = 0
            currentTimeDiff = time.time() - self.startAt
            progress = currentTimeDiff / self.during
            if progress >= 1.0:
                self.isRunning = False
                progress = 1.0
            for angle in self.startAngles:
                self.currentAngle[i] = self.startAngles[i] + self.diffAngle * progress
            i += 1
            self.callback(self.currentAngle)
            time.sleep(0.1)
