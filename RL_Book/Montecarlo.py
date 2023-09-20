import matplotlib.pyplot as plt
import random
from matplotlib.patches import Rectangle

# 다트를 던질 횟수 설정
num_darts_list = [1, 100, 10000, 1000000]

# 그래프 초기화
fig, axs = plt.subplots(1, 4, figsize=(16, 4))

# 각각의 그래프에 대해 반복
for i, num_darts in enumerate(num_darts_list):
    # 원 안에 떨어진 다트의 개수 초기화
    num_darts_inside_circle = 0

    # 붉은 색 점 개수와 파란 색 점 개수 초기화
    num_red_dots = 0
    num_blue_dots = 0

    # 원 그리기
    circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='none', linestyle='dotted')

    # 사각형 그리기
    rect = Rectangle((-1, -1), 2, 2, edgecolor='black', facecolor='none', linestyle='dotted')
    axs[i].add_patch(rect)

    # x축과 y축 그리기
    axs[i].add_artist(circle)
    axs[i].axhline(0, color='black', linewidth=0.5)
    axs[i].axvline(0, color='black', linewidth=0.5)

    # 점 생성 및 원 안에 있는지 확인
    for _ in range(num_darts):
        # 다트의 좌표 랜덤 생성
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        # 다트가 원 안에 있는지 확인
        if x ** 2 + y ** 2 <= 1:
            num_darts_inside_circle += 1
            num_red_dots += 1
            # 원 안에 있는 다트는 붉은 색으로 표시
            axs[i].plot(x, y, 'ro', markersize=1)
        else:
            num_blue_dots += 1
            # 원 밖에 있는 다트는 파란색으로 표시
            axs[i].plot(x, y, 'bo', markersize=1)

    # 원의 넓이 추정 4 = 2 * 2 (사각형의 넓이)
    circle_area = 4 * (num_darts_inside_circle / num_darts)

    # 그래프 설정
    axs[i].set_aspect('equal')
    axs[i].set_xlim(-1.3, 1.3)
    axs[i].set_ylim(-1.3, 1.3)

    # 추정된 원의 넓이와 붉은 색/파란 색 점 개수 표시
    text_content_1 = f"Space: {circle_area:.4f}\n"
    axs[i].text(-1.0, 1.0, text_content_1, fontsize=10)

    text_content_2 = f"Red dot: {num_red_dots}\n"
    axs[i].text(-1.0, -1.3, text_content_2, fontsize=10)

    # 그래프 제목 설정
    axs[i].set_title(f"Number of Darts: {num_darts}")

# 그래프 표시
plt.tight_layout()
plt.show()
