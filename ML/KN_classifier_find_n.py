# Model
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import data

# Data
fish_length = data.bream_length + data.smelt_length
fish_weight = data.bream_weight + data.smelt_length

fish_data = list(zip(fish_length, fish_weight))

max_score = 0
# 적절한 이웃 개수 찾기

for i in range(1, 50):
    kn = KNeighborsClassifier(n_neighbors=i)
    kn.fit(fish_data, data.fish_target)
    score = kn.score(fish_data, data.fish_target)
    if score >= max_score:
        max_score = score
    print("kn%d Score : %lf" % (i, score))

print(max_score)

# 모델 생성
kn5 = KNeighborsClassifier()
kn5.fit(fish_data, data.fish_target)
score5 = kn5.score(fish_data, data.fish_target)

# 예측 결과 출력
res_kn5 = kn5.predict([(10, 900)])
print(res_kn5)

plt.scatter(fish_length, fish_weight)
plt.scatter(10, 900, marker='^')
plt.show()
