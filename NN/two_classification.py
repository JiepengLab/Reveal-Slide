import numpy as np
import matplotlib.pyplot as plt
import copy

np.random.seed(2333)


# Boundary Display

def plot_decision_boundary(model, X, y):
    x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
    y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
    h = 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = model(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.scatter(X[0, :], X[1, :], c=y, cmap=plt.cm.Spectral)
    plt.show()


# Basic Function

def sigmoid(z):
    s = 1 / (1 + np.exp(-z))
    return s

def initialization(dim):
    w = np.random.randn(dim, 1) * 0.01
    b = 0.0
    return w, b

def propagate(w, b, X, Y):
    m = X.shape[1]
    z = np.dot(w.T, X) + b     # broadcasting
    A = sigmoid(z)
    cost = -1 / m * (np.sum(np.dot(Y, np.log(A).T)) + np.sum(np.dot((1 - Y), np.log(1 - A).T)))
    db = 1 / m * np.sum(A - Y)
    dw = 1 / m * np.dot(X, (A - Y).T)
    cost = np.squeeze(np.array(cost))
    grads = {"dw": dw, "db": db}
    return grads, cost


def optimize(w, b, X, Y, num_iterations = 100, learning_rate = 0.009):
    w = copy.deepcopy(w)
    b = copy.deepcopy(b)
    costs = []
    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)
        dw = grads["dw"]
        db = grads["db"]
        w = w - learning_rate * dw
        b = b - learning_rate * db
    params = {"w": w   , "b": b  }
    grads  = {"dw": dw , "db": db}
    return params, grads, costs

def predict(w, b, X):

    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)
    
    A = sigmoid(np.dot(w.T, X) + b)
    
    for i in range(A.shape[1]):
        if A[0, i] > 0.5:
            Y_prediction[0, i] = 1
        else:
            Y_prediction[0, i] = 0
    
    return Y_prediction


def data_generation(num, k, b, scale_x, scale_y, noise_lev):

    x       = np.random.rand(1, num)  * scale_x
    x_noise = np.random.randn(1, num) * scale_x * noise_lev

    y       = np.random.rand(1, num)  * scale_y
    y_noise = np.random.randn(1, num) * scale_y * noise_lev

    X_train = np.concatenate((x, y), axis = 0)
    X_judge = np.concatenate((x_noise, y_noise), axis = 0) + X_train

    Y_train = np.zeros(num)

    # print(X_judge)

    for i in range(0, num):
        if (X_judge[0][i] * k + b > X_judge[1][i]):
            Y_train[i] = 1
        else:
            Y_train[i] = 0

    return X_train, Y_train


# Main Function

X_train, Y_train = data_generation(500, 0.87, 12, 100, 100, 0.05); # <--- You can change the parameters here

blue_indices = np.where(Y_train == 0)[0]
red_indices  = np.where(Y_train == 1)[0]

plt.scatter(X_train[0, blue_indices], X_train[1, blue_indices], c = 'blue', label = 'class 0')
plt.scatter(X_train[0, red_indices] , X_train[1, red_indices] , c = 'red' , label = 'class 1')
plt.show()

w, b = initialization(X_train.shape[0])

parameters, grads, costs = optimize(w, b, X_train, Y_train, 10000, 0.008)
    
w = parameters["w"]
b = parameters["b"]

plot_decision_boundary(lambda x: predict(w, b, x.T), X_train, Y_train)