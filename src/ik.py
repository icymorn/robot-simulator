from math import pi, atan2, acos, cos, sin, sqrt
from loader import config

_to_rad = pi / 180
_to_deg = 180 / pi

_l1 = config.joint[1].r
_l2 = config.joint[3].r

def ik(x, y):
    l3_2 = x**2 + y**2
    l3   = sqrt(l3_2)
    theta2 = pi - acos((_l1**2 + _l2**2 - l3_2) / (2 * _l1 * _l2))
    theta1b = atan2(y, x)
    theta1a = acos((_l1**2 + l3_2 - _l1**2) / (2 * _l1 * l3))
    theta1  = theta1a + theta1b
    theta3  = (pi - theta2) - (pi / 2 - theta1)
    return (theta1, theta2, theta3)

# print [rad * _to_deg for rad in ik(0.1, 0.1)]