import numpy as np
import matplotlib.pyplot as plt
import copy

np.random.seed(1)


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

def layer_sizes(X, Y):
    n_x = X.shape[0]
    n_h = 4
    n_y = Y.shape[0]
    return (n_x, n_h, n_y)

def initialize_parameters(n_x, n_h, n_y):
    np.random.seed(2) 
    W1 = np.random.randn(n_h, n_x) * 0.4
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.4
    b2 = np.zeros((n_y, 1))
    assert (W1.shape == (n_h, n_x))
    assert (b1.shape == (n_h, 1))
    assert (W2.shape == (n_y, n_h))
    assert (b2.shape == (n_y, 1))
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    return parameters

def forward_propagation(X, parameters):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    Z1 = np.dot(W1, X) + b1
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2, A1) + b2
    # print(A1.shape)
    # print(W2.shape)
    # print(Z2.shape)
    A2 = sigmoid(Z2)
    assert(A2.shape == (1, X.shape[1]))
    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}
    return A2, cache

def compute_cost(A2, Y, parameters):
    m = Y.shape[1]
    logprobs = np.multiply(Y, np.log(A2)) + np.multiply(1 - Y, np.log(1 - A2))
    cost = -1 / m * np.sum(logprobs)
    cost = np.squeeze(cost)
    assert(isinstance(cost, float))
    return cost

def backward_propagation(parameters, cache, X, Y):
    m = X.shape[1]
    W1 = parameters["W1"]
    W2 = parameters["W2"]
    A1 = cache["A1"]
    A2 = cache["A2"]
    dZ2 = A2 - Y
    dW2 = 1 / m * np.dot(dZ2, A1.T)
    db2 = 1 / m * np.sum(dZ2, axis = 1, keepdims = True)
    dZ1 = np.multiply(np.dot(W2.T, dZ2), 1 - np.power(A1, 2))
    dW1 = 1 / m * np.dot(dZ1, X.T)
    db1 = 1 / m * np.sum(dZ1, axis = 1, keepdims = True)
    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}
    return grads

def update_parameters(parameters, grads, learning_rate = 1.2):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    return parameters

def nn_model(X, Y, n_h, num_iterations = 10000, print_cost = True):
    np.random.seed(3)
    n_x = layer_sizes(X, Y)[0]
    n_y = layer_sizes(X, Y)[2]

    parameters = initialize_parameters(n_x, n_h, n_y)
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    for i in range(0, num_iterations):
        A2, cache = forward_propagation(X, parameters)
        cost = compute_cost(A2, Y, parameters)
        grads = backward_propagation(parameters, cache, X, Y)
        parameters = update_parameters(parameters, grads, learning_rate = 0.004)
        if print_cost and i % 1000 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))

    return parameters

def predict(parameters, X):
    predictions, cache = forward_propagation(X, parameters)
    predictions = (predictions > 0.5)
    return predictions


# Data Generation

def data_generation(num, scale_x, scale_y, sep_x, sep_y, noise_lev):

    x       = np.random.rand(1, num)  * scale_x
    x_noise = np.random.randn(1, num) * scale_x * noise_lev

    y       = np.random.rand(1, num)  * scale_y
    y_noise = np.random.randn(1, num) * scale_y * noise_lev

    X_train = np.concatenate((x, y), axis = 0)
    X_judge = np.concatenate((x_noise, y_noise), axis = 0) + X_train

    Y_train = np.zeros(num)

    # print(X_judge)

    for i in range(0, num):
        if (X_judge[0][i] > scale_x * sep_x and X_judge[1][i] > scale_y * sep_y):
            Y_train[i] = 1
        elif (X_judge[0][i] < scale_x * sep_x and X_judge[1][i] < scale_y * sep_y):
            Y_train[i] = 1
        else:
            Y_train[i] = 0

    return X_train, Y_train


# Main Function

X_train, Y_train = data_generation(1000, 100, 100, 0.6, 0.4, 0.02); # <--- You can change the parameters here

blue_indices = np.where(Y_train == 0)[0]
red_indices  = np.where(Y_train == 1)[0]

plt.scatter(X_train[0, blue_indices], X_train[1, blue_indices], c = 'blue', label = 'class 0')
plt.scatter(X_train[0, red_indices] , X_train[1, red_indices] , c = 'red' , label = 'class 1')
plt.show()

Y_train = np.expand_dims(Y_train, 0)

parameters = nn_model(X_train, Y_train, n_h = 12, num_iterations = 40000)

# Plot the decision boundary
plot_decision_boundary(lambda x: predict(parameters, x.T), X_train, Y_train[0, :])