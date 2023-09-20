import pygame
import random
import numpy as np
import matplotlib.pyplot as plt

# q테이블 대신에 함수, DNN을 사용하면, 용량을 줄일 수 있음. [바닥부터 배우는 강화학습 p187]

pygame.init()

# 화면 크기 설정
screen_width = 50
screen_height = 50
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 타이틀 설정
pygame.display.set_caption("지렁이 게임")

# FPS
clock = pygame.time.Clock()

# 색깔
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 지렁이 초기 위치 설정
snake_x = screen_width / 2
snake_y = screen_height / 2

# 먹이 초기 위치 설정
food_x = round(random.randrange(0, screen_width - 10) / 10.0) * 10.0
food_y = round(random.randrange(0, screen_height - 10) / 10.0) * 10.0

# 학습 과정에서 얻은 보상을 저장하는 리스트
total_rewards = []

# 지렁이 이동 방향 초기 설정
direction_x = 0
direction_y = 0

# 보상
REWARD_EAT_FOOD = 1
REWARD_MOVE = -0.01

# Q-Learning
Q_TABLE_SIZE = 20
ALPHA = 0.5
GAMMA = 0.9
EPSILON = 0.1
Q_TABLE = np.zeros((Q_TABLE_SIZE, Q_TABLE_SIZE, 4))

# 게임 오버
def game_over():
    font = pygame.font.SysFont(None, 25)
    text = font.render("게임 오버, 다시 시작하려면 스페이스바를 누르세요", True, WHITE)
    screen.blit(text, [screen_width / 6, screen_height / 3])
    pygame.display.update()

    # 스페이스바를 누르면 게임 재시작
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

# 상태(state) 정의
def get_state():
    state_x = int(snake_x / (screen_width / Q_TABLE_SIZE))
    state_y = int(snake_y / (screen_height / Q_TABLE_SIZE))
    food_state_x = int(food_x / (screen_width / Q_TABLE_SIZE))
    food_state_y = int(food_y / (screen_height / Q_TABLE_SIZE))
    state = (state_x, state_y, food_state_x, food_state_y)
    return state

# 행동(action) 정의
def get_action(state):
    if np.random.rand() < EPSILON:
        action = np.random.randint(0, 4)
    else:
        action = np.argmax(Q_TABLE[state])
    return action

# Q-테이블(Q-table) 초기화
def init_q_table():
    global Q_TABLE
    Q_TABLE = np.zeros((Q_TABLE_SIZE, Q_TABLE_SIZE, Q_TABLE_SIZE, Q_TABLE_SIZE, 4))

# Q-테이블(Q-table) 업데이트
def update_q_table(prev_state, action, state, reward):
    max_q = np.max(Q_TABLE[state])
    Q_TABLE[prev_state][action] += ALPHA * (reward + GAMMA * max_q - Q_TABLE[prev_state][action])

# 게임 루프
def game_loop():
    global direction_x, direction_y, snake_x, snake_y, food_x, food_y

    game_exit = False
    game_over_flag = False

    # 보상 초기화
    total_reward = 0

    # Q-Learning 초기화
    init_q_table()

    episode = 0

    while not game_exit:

        # 게임 오버 처리
        #while game_over_flag:
        #    game_over()

        # 상태 관측
        prev_state = get_state()

        # 행동 선택
        action = get_action(prev_state)

        # 이전 위치 저장
        prev_snake_x = snake_x
        prev_snake_y = snake_y

        # 행동 실행
        if action == 0:
            direction_x = -10
            direction_y = 0
        elif action == 1:
            direction_x = 10
            direction_y = 0
        elif action == 2:
            direction_y = -10
            direction_x = 0
        elif action == 3:
            direction_y = 10
            direction_x = 0

        # 지렁이 이동 처리
        snake_x += direction_x
        snake_y += direction_y

        # 벽 충돌 처리
        if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
            game_over_flag = False
        if snake_x < 0:
            snake_x = 0
        if snake_x >= screen_width:
            snake_y = screen_width
        if snake_y < 0:
            snake_y = 0
        if snake_y >= screen_height:
            snake_y = screen_height

        # 먹이 먹기
        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(0, screen_width - 10) / 10.0) * 10.0
            food_y = round(random.randrange(0, screen_height - 10) / 10.0) * 10.0
            total_reward += REWARD_EAT_FOOD

        # 이동 보상
        else:
            total_reward += REWARD_MOVE

        # 새로운 상태 관측
        state = get_state()

        # Q-테이블 업데이트
        update_q_table(prev_state, action, state, total_reward)

        # 총 보상(total_reward) 출력
        print("Episode:", episode, "Total Reward:", total_reward)

        # 에피소드(episode) 증가
        episode += 1

        # 학습 과정에서 얻은 보상 저장
        total_rewards.append(total_reward)

        # 화면에 그리기
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, 10, 10])
        pygame.draw.rect(screen, WHITE, [snake_x, snake_y, 10, 10])
        pygame.display.update()

        # FPS 설정
        clock.tick(20)

    pygame.quit()
    quit()

# 게임 실행
game_loop()

# 그래프 그리기
plt.plot(total_rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Reward per Episode')
plt.show()
