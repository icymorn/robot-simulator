import numpy as np
from math import cos, sin, pi


def toRadian(degree):
    return pi * degree / 180


class DHMatrix:

    def __init__(self, theta, d, r, alpha, prev = None, next = None):
        self.theta = toRadian(theta)
        self.d     = d
        self.r     = r
        self.alpha = toRadian(alpha)
        self.m     = np.mat(np.eye(4))
        self.prev  = prev
        self.next  = next

    def matrix(self):
        return self.m

    def transform(self):
        cosTheta = cos(self.theta)
        sinTheta = sin(self.theta)
        sinAlpha = sin(self.alpha)
        cosAlpha = cos(self.alpha)
        return np.mat([
            [cosTheta, -sinTheta * cosAlpha, sinTheta * cosAlpha , self.r * cosTheta],
            [sinTheta, cosTheta * cosAlpha , -cosTheta * sinAlpha, self.r * sinTheta],
            [0       , sinAlpha            , cosAlpha            , self.d],
            [0       , 0                   , 0                   , 1]
        ])

    def transD(self):
        pass

    def transR(self):
        pass

    def RotAphla(self):
        pass

    def RotTheta(self):
        pass

    def setTheta(self, theta):
        self.theta = theta

    def setTransD(self, d):
        self.d = d

    def setAlpha(self, alpha):
        self.alpha = alpha

    def setR(self, r):
        self.r = r

    def setPrev(self, prev):
        self.prev = prev

    def setNext(self, next):
        self.next = next

if __name__ == '__main__':
    base = DHMatrix(0, 0, 0, 0)
    m1 = DHMatrix(0, 0.3, 0, 90)
    m2 = DHMatrix(45, 0.2, 0.3, 0)
    m3 = DHMatrix(45, 0.2, 0.3, 0)
    print base.transform() * m1.transform()
    print m1.transform() * m2.transform()
    print m1.transform() * m2.transform() * m3.transform()