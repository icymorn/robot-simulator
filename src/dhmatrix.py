import numpy as np
from math import cos, sin, pi


def toRadian(degree):
    return pi * degree / 180


class DHMatrix:

    def __init__(self, theta, d, r, alpha, scale = 1, offset = 0, bindPort = None):
        self.theta = toRadian(theta)
        self.d     = d
        self.r     = r
        self.alpha = toRadian(alpha)
        self.scale = scale
        self.offset = offset
        self.bindPort = bindPort

    def matrix(self):
        return self.m

    def transform(self):
        cosTheta = cos(self.theta)
        sinTheta = sin(self.theta)
        sinAlpha = sin(self.alpha)
        cosAlpha = cos(self.alpha)
        return np.mat([
            [cosTheta, -sinTheta * cosAlpha, sinTheta * sinAlpha , self.r * cosTheta],
            [sinTheta, cosTheta * cosAlpha , -cosTheta * sinAlpha, self.r * sinTheta],
            [0       , sinAlpha            , cosAlpha            , self.d],
            [0       , 0                   , 0                   , 1]
        ])

    def matrixFirst(self):
        pass

    def iniM(self):
        self.m = np.mat(np.eye(4))
        return self

    def transD(self):
        self.m = self.m * [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, self.d], [0, 0, 0, 1]]
        return self

    def transR(self):
        self.m = self.m * [[1, 0, 0, self.r], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        return self

    def rotAlpha(self):
        sinAlpha = sin(self.alpha)
        cosAlpha = cos(self.alpha)
        self.m = self.m * [[1, 0, 0, 0], [0, cosAlpha, -sinAlpha, 0], [0, sinAlpha, cosAlpha, 0], [0, 0, 0, 1]]
        return self

    def rotTheta(self):
        theta = self.scale * self.theta + self.offset
        cosTheta = cos(theta)
        sinTheta = sin(theta)
        self.m = self.m * [[cosTheta, -sinTheta, 0, 0], [sinTheta, cosTheta, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        return self

    def setTheta(self, theta):
        self.theta = theta

    def setTransD(self, d):
        self.d = d

    def setAlpha(self, alpha):
        self.alpha = alpha

    def setR(self, r):
        self.r = r


if __name__ == '__main__':
    base = DHMatrix(0, 0, 0, 0)
    m1 = DHMatrix(0, 0.3, 0, 90)
    m2 = DHMatrix(45, 0.2, 0.3, 0)
    m3 = DHMatrix(45, 0.2, 0.3, 0)
    # print base.transform() * m1.transform()
    # print m1.transform() * m2.transform()
    m = m2.transform()
    print m
    m_x = m2.iniM().transD().rotTheta().transR().rotAlpha().m
    print m_x