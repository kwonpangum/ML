#물속에서 SONAR를 사용하여 동전을 탐지하는 인공지능

#1. 인공지능 환경 만들기

from keras.models import Sequential
from keras.layers import Dense

import pandas as pd

from sklearn.model_selection import train_test_split

#2. 데이터를 불러오고, 인공지능이 학습을 할 수 있도록 가공 (학습용 데이터 vs. 테스트용 데이터)

df = pd.read_csv('Find_Coin_in_the_Water_PK.csv')

X = df.iloc[:, 0:60]
y = df.iloc[:, 60]

y = pd.get_dummies(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True)

#3. 인공지능 모델 만들기
model = Sequential()
model.add(Dense(12, input_dim=60, activation='relu', name='Dense_1'))
model.add(Dense(8, activation='relu', name='Dense_2'))
model.add(Dense(2, activation='sigmoid', name='Dense_3'))

model.summary()

#4. '학습용 데이터'를 이용하여 '인공지능 모델' 학습시키기

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=200, batch_size=10)

#5. '테스트용 데이터'를 이용하여 '학습된 인공지능 모델'의 정확도를 확인하기

score = model.evaluate(X_test, y_test)
print('\n-----------------------')
print('모델의 정확도는', score[1], '입니다.')
