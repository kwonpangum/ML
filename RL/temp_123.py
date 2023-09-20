import pygame
import random
import numpy as np
from collections import defaultdict
import math
import matplotlib.pyplot as plt

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 배경화면 설정 및 초기화
WIDTH = 600
HEIGHT = 600
FPS = 30
SHIP_RADIUS = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen.fill(WHITE)

# 에피소드 변수 초기화
episode_count = 0


# 텍스트 함수 설정
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# 함포 클래스 설정
class Cannonball(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.radius = 2
        self.color = color
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 25

    # 함정의 중앙에 함포 위치
    def move(self, speed_x, speed_y):
        self.rect.x += speed_x
        self.rect.y += speed_y


# 전투함 클래스 설정
class BattleShip(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.radius = 5
        self.color = color
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = 0.2
        self.cannonball = Cannonball(self.rect.centerx - self.radius, self.rect.centery - self.radius, self.color)
        self.cannonball_fired = False

    def fire_cannonball_toward_enemy(self, target_x, target_y):
        if not self.cannonball_fired:
            self.cannonball_fired = True
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            angle = math.atan2(dy, dx)
            self.cannonball.speed_x = self.cannonball.speed * math.cos(angle)
            self.cannonball.speed_y = self.cannonball.speed * math.sin(angle)
            self.cannonball.rect.x = self.rect.centerx
            self.cannonball.rect.y = self.rect.centery

    def action_to_move(self, action):
        if action == 0:
            return 0, 0  # Stay
        elif action == 1:
            return -1, 0  # Move left
        elif action == 2:
            return 1, 0  # Move right
        elif action == 3:
            return 0, -1  # Move up
        elif action == 4:
            return 0, 1  # Move down
        elif action == 5:
            return -1, -1  # Move left and up
        elif action == 6:
            return 1, -1  # Move right and up
        elif action == 7:
            return -1, 1  # Move left and down
        elif action == 8:
            return 1, 1  # Move right and
        else:
            return 0, 0  # Default to stay

    def update(self, action):
        self.speed_x, self.speed_y = self.action_to_move(action)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 경계 처리
        self.rect.x = max(0, min(WIDTH - SHIP_RADIUS * 2, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - SHIP_RADIUS * 2, self.rect.y))

        self.update_cannonball()

    def update_cannonball(self):
        if self.cannonball_fired:
            self.cannonball.move(self.cannonball.speed_x, self.cannonball.speed_y)
            if self.cannonball.rect.y < -self.cannonball.radius * 2 or \
                    self.cannonball.rect.y > HEIGHT or \
                    self.cannonball.rect.x < -self.cannonball.radius * 2 or \
                    self.cannonball.rect.x > WIDTH:
                self.cannonball_fired = False


# 코드 최적화: random_move() 함수를 클래스의 메소드로 이동
our_ship = BattleShip(300, 500, BLUE)
enemy_ship = BattleShip(300, 100, RED)
all_sprites = pygame.sprite.Group(our_ship, enemy_ship)


def random_move():
    speed_x = random.choice([-1, 0, 1])
    speed_y = random.choice([-1, 0, 1])
    return speed_x, speed_y


def reset_game():
    global our_ship, enemy_ship
    our_ship = BattleShip(300, 500, BLUE)
    enemy_ship = BattleShip(300, 100, RED)
    return (our_ship.rect.x, our_ship.rect.y, enemy_ship.rect.x, enemy_ship.rect.y)


enemy_fired_first = False


def step(state, action):
    global our_ship, enemy_ship, enemy_fired_first

    x1, y1, x2, y2 = state

    # Our ship movement
    our_ship.speed_x, our_ship.speed_y = our_ship.action_to_move(action)
    our_ship.update(action)

    # Enemy ship movement and fire
    enemy_ship.speed_x, enemy_ship.speed_y = random_move()
    enemy_action = random.randint(0, 12)
    enemy_ship.update(enemy_action)

    # Add a condition to fire cannonball with a probability
    if random.random() < 0.5:
        enemy_ship.fire_cannonball_toward_enemy(our_ship.rect.x, our_ship.rect.y)
        enemy_fired_first = True

    # Fire cannonball if action is 9, 10, 11, or 12 and enemy_fired_first is True
    if action in [9, 10, 11, 12] and enemy_fired_first:
        our_ship.fire_cannonball_toward_enemy(enemy_ship.rect.x, enemy_ship.rect.y)

    # Check for collisions
    hit_enemy = pygame.sprite.collide_circle(our_ship.cannonball, enemy_ship)
    hit_us = pygame.sprite.collide_circle(enemy_ship.cannonball, our_ship)

    reward = 0
    done = False

    if hit_enemy:
        reward = +5
        done = True
    elif hit_us:
        reward = -1
        done = True
    elif enemy_ship.cannonball_fired and not our_ship.cannonball_fired:
        reward = -0.1

    next_state = (our_ship.rect.x, our_ship.rect.y, enemy_ship.rect.x, enemy_ship.rect.y)

    return next_state, reward, done


def q_learning(alpha, gamma, epsilon, num_episodes, visualize_every=100):
    global episode_count, our_ship, enemy_ship

    q_table = defaultdict(lambda: np.zeros(13))
    cumulative_reward = 0
    episode_rewards = []  # 에피소드마다 보상을 저장할 리스트 추가
    episode_numbers = []  # 에피소드 번호를 저장할 리스트 추가

    our_ship_wins = 0
    enemy_ship_wins = 0
    our_ship_win_rates = []
    enemy_ship_win_rates = []

    # 그래프를 그리기 위한 초기화
    plt.ion()
    fig, ax = plt.subplots()
    line1, = ax.plot(episode_numbers, our_ship_win_rates, color='blue', label='우군 전투함 승률')
    line2, = ax.plot(episode_numbers, enemy_ship_win_rates, color='red', label='적군 전투함 승률')

    for episode in range(num_episodes):
        episode_count += 1
        state = reset_game()

        our_ship = BattleShip(state[0], state[1], BLUE)
        enemy_ship = BattleShip(state[2], state[3], RED)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(our_ship)
        all_sprites.add(enemy_ship)

        done = False
        while not done:
            if np.random.rand() < epsilon:
                action = np.random.randint(0, 12)
            else:
                action = np.argmax(q_table[state])

            next_state, reward, done = step(state, action)
            q_table[state][action] += alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state][action])
            state = next_state

            cumulative_reward += reward

            if episode % visualize_every == 50:
                screen.fill(WHITE)
                all_sprites.draw(screen)
                if our_ship.cannonball_fired:
                    screen.blit(our_ship.cannonball.image, our_ship.cannonball.rect)
                if enemy_ship.cannonball_fired:
                    screen.blit(enemy_ship.cannonball.image, enemy_ship.cannonball.rect)

                pygame.display.set_caption(
                    f"AI 전투함 | Episode: {episode_count} | Cumulative Reward: {cumulative_reward}")
                pygame.display.flip()
                clock.tick(FPS)

        if reward > 0:
            our_ship_wins += 1
        else:
            enemy_ship_wins += 1

        our_ship_win_rate = our_ship_wins / (episode + 1)
        enemy_ship_win_rate = enemy_ship_wins / (episode + 1)

        our_ship_win_rates.append(our_ship_win_rate)
        enemy_ship_win_rates.append(enemy_ship_win_rate)
        episode_numbers.append(episode_count)

        if episode % 200 == 0:
            print(f"Episode {episode} completed. Cumulative Reward: {cumulative_reward}")

        # 그래프 업데이트
        line1.set_xdata(episode_numbers)
        line1.set_ydata(our_ship_win_rates)
        line1.set_label("AI BattleShip")
        line2.set_xdata(episode_numbers)
        line2.set_ydata(enemy_ship_win_rates)
        line2.set_label("EnemyShip")
        ax.set_xlabel('Number of Episode')
        ax.set_ylabel('Average number wins')
        ax.relim()
        ax.autoscale_view()
        ax.legend(loc='upper right')
        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.ioff()
    plt.show()

    return q_table


# 학습 파라미터 입력
alpha = 0.1
gamma = 0.99
epsilon = 0.5  # 0이면 greedy, 1이면 모든 행동 무작위로 선택
num_episodes = 300000

# 학습 및 시각화
q_table = q_learning(alpha, gamma, epsilon, num_episodes)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    state = (our_ship.rect.x, our_ship.rect.y, enemy_ship.rect.x, enemy_ship.rect.y)
    action = np.argmax(q_table[state])
    next_state, reward, done = step(state, action)

    # 전투함 위치 업데이트
    our_ship.rect.x, our_ship.rect.y, enemy_ship.rect.x, enemy_ship.rect.y = next_state

    screen.fill(WHITE)
    all_sprites.draw(screen)
    if enemy_ship.cannonball_fired:
        screen.blit(enemy_ship.cannonball.image, enemy_ship.cannonball.rect)
    if our_ship.cannonball_fired:
        screen.blit(our_ship.cannonball.image, our_ship.cannonball.rect)

    # 배경창 제목에 에피소드 횟수와 누적 보상치 표시
    pygame.display.set_caption(f"AI 전투함 | Episode: {episode_count} | Cumulative Reward: {cumulative_reward}")

    pygame.display.flip()

pygame.quit()
