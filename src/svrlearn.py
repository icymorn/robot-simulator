"""
===================================================================
Support Vector Regression (SVR) using linear and non-linear kernels
===================================================================
  
Toy example of 1D regression using linear, polynominial and RBF
kernels.
  
"""
print __doc__
  
###############################################################################
# Generate sample data
import numpy as np


def chart(data):
    x_lines = [p[0] for p in data]
    y_lines = [p[1] for p in data]

x_base = [x for x in range(90)]

X = np.sort(np.matrix(x_base), axis=0)
y = np.sin(X).ravel()

print y
###############################################################################
# Add noise to targets
y[::5] += 3*(0.5 - np.random.rand(8))

print y

###############################################################################
# Fit regression model
from sklearn.svm import SVR

svr_rbf = SVR(kernel='rbf', C=1e4, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e4)
svr_poly = SVR(kernel='poly', C=1e4, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(X)
y_lin = svr_lin.fit(X, y).predict(X)
y_poly = svr_poly.fit(X, y).predict(X)


###############################################################################
# look at the results
import pylab as pl
pl.scatter(X, y, c='k', label='data')
pl.hold('on')
pl.plot(X, y_rbf, c='g', label='RBF model')
pl.plot(X, y_lin, c='r', label='Linear model')
pl.plot(X, y_poly, c='b', label='Polynomial model')
pl.xlabel('data')
pl.ylabel('target')
pl.title('Support Vector Regression')
pl.legend()
pl.show()

if __name__ == '__main__':
    chart([(0, 0.1),(5, 0.15),(10,0.3),(15,0.4),(20,0.5),(25,0.65),(30,0.8),(35,0.90),(40,0.95),(45,0.97),(50,0.99),(55,0.995),(60,0.9995)])