# 시그모이드, 하이퍼볼릭탄젠트, 렐루 함수

import matplotlib.pyplot as plt
import numpy as np

# sigmoid 함수
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# tanh 함수
def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    return 1 - np.tanh(x)**2

# ReLU 함수
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x <= 0, 0, 1)  #x가 0보다 작거나 같으면 0을, 0보다 크면 1을 반환

# x 값 범위 설정
x = np.arange(-7, 7, 0.01)

# 시그모이드 함수 및 미분 함수 그래프
plt.subplot(3, 1, 1)
plt.plot(x, sigmoid(x), label='Sigmoid')
plt.plot(x, sigmoid_derivative(x), label='Sigmoid Derivative')
plt.legend()
plt.title('Sigmoid Function and Derivative')

# 하이퍼볼릭탄젠트 함수 및 미분 함수 그래프
plt.subplot(3, 1, 2)
plt.plot(x, tanh(x), label='Hyperbolic Tangent')
plt.plot(x, tanh_derivative(x), label='Hyperbolic Tangent Derivative')
plt.legend()
plt.title('Hyperbolic Tangent Function and Derivative')

# 렐루 함수 및 미분 함수 그래프
plt.subplot(3, 1, 3)
plt.plot(x, relu(x), label='ReLU')
plt.plot(x, relu_derivative(x), label='ReLU Derivative')
plt.legend()
plt.title('ReLU Function and Derivative')

plt.tight_layout()
plt.show()

