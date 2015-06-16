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

def get_predict(data):
    x_lines = np.array([[p[0]] for p in data])
    # y_lines = np.sin(x_lines).ravel()
    y_lines = np.array([p[1] for p in data])

    from sklearn.svm import SVR

    svr_rbf = SVR(kernel='rbf', C=1e4, gamma=0.1)
    # svr_lin = SVR(kernel='linear', C=1e4)
    # svr_poly = SVR(kernel='poly', C=1e4, degree=2)
    y_rbf = svr_rbf.fit(x_lines, y_lines).predict(x_lines)
    # y_lin = svr_lin.fit(x_lines, y_lines).predict(x_lines)
    # y_poly = svr_poly.fit(x_lines, y_lines).predict(x_lines)
    return x_lines.ravel(), y_rbf.ravel()


def chart(data):
    x_lines = np.array([[p[0]] for p in data])
    # y_lines = np.sin(x_lines).ravel()
    y_lines = np.array([p[1] for p in data])

    from sklearn.svm import SVR

    svr_rbf = SVR(kernel='rbf', C=1e4, gamma=0.1)
    # svr_lin = SVR(kernel='linear', C=1e4)
    # svr_poly = SVR(kernel='poly', C=1e4, degree=2)
    y_rbf = svr_rbf.fit(x_lines, y_lines).predict(x_lines)
    # y_lin = svr_lin.fit(x_lines, y_lines).predict(x_lines)
    # y_poly = svr_poly.fit(x_lines, y_lines).predict(x_lines)

    import pylab as pl
    pl.scatter(x_lines, y_lines, c='k', label='data')
    pl.hold('on')
    pl.plot(x_lines, y_rbf, c='g', label='RBF model')
    # pl.plot(x_lines, y_lin, c='r', label='Linear model')
    # pl.plot(x_lines, y_poly, c='b', label='Polynomial model')
    pl.xlabel('data')
    pl.ylabel('target')
    pl.title('Support Vector Regression')
    pl.legend()
    pl.show()
    return x_lines.ravel(), y_rbf.ravel()

def get_y(x_lines, y_rbf, input):
    for i in range(len(x_lines)):
        if input <= x_lines[i]:
            x1 = x_lines[i]
            x2 = x_lines[i + 1]
            y1 = y_rbf[i]
            y2 = y_rbf[i + 1]
            print x1, x2, y1, y2
            return (x1 - input) * (y2 - y1) / (x2 - x1) + y1

if __name__ == '__main__':
    x, y = chart([(0, 0.1),(5, 0.15),(10,0.3),(15,0.4),(20,0.5),(25,0.65),(30,0.8),(35,0.90),(40,0.95),(45,0.97),(50,0.99),(55,0.995),(60,0.9995)])
    print get_y(x, y, 18)
