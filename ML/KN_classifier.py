import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import data

length = data.bream_length + data.smelt_length
weight = data.bream_weight + data.smelt_weight

fish_data = list([i, j] for i, j in zip(length, weight))

kn = KNeighborsClassifier(n_neighbors=5)

kn.fit(fish_data, data.fish_target)

res = kn.score(fish_data, data.fish_target)
print("모델의 정확도 :", res)
'''
print(kn._fit_X)
print(kn._y)
'''

res = kn.predict([[10, 30], [30, 600]])
print("예측결과(0: 빙어, 1: 도미):", res)

plt.scatter(data.bream_length, data.bream_weight)
plt.scatter(data.smelt_length, data.smelt_weight)
plt.scatter(10, 30, marker='^')
plt.scatter(30, 600, marker='^')
plt.xlabel("length")
plt.ylabel("weight")
plt.show()
