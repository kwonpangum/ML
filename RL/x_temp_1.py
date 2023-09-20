import pygame
import numpy as np
import math
import random
# 게임 환경 설정
WIDTH, HEIGHT = 600, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
LINE_WIDTH = 1

class Ship:
    def __init__(self, screen, color, position):
        self.screen = screen
        self.color = color
        self.position = position
        self.radius = 5

        # 초기 각도 (방향) 설정
        if color == (255, 0, 0):  # RED
            self.angle = 270
        elif color == (0, 0, 255):  # BLUE
            self.angle = 90
        elif color == (128, 128, 128):  # GRAY
            self.angle = random.randint(0, 360)
        else:
            self.angle = 0

        self.speed = 5  # 움직이는 속도
        self.cannon = Cannonball()  # Cannon 객체 생성
#        self.radar = Radar()  # Radar 객체 생성

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.radius)

        # 이동 방향을 표시하는 선분 그리기
        end_x = self.position[0] + 2 * self.speed * math.cos(math.radians(self.angle))
        end_y = self.position[1] - 2 * self.speed * math.sin(math.radians(self.angle))
        pygame.draw.line(self.screen, self.color, self.position, (end_x, end_y), 2)

    def move_forward(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.position = (self.position[0] + dx, self.position[1] - dy)

    def move_backward(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.position = (self.position[0] - dx, self.position[1] + dy)

    def turn_left(self, degrees):
        self.angle = (self.angle + degrees) % 360

    def turn_right(self, degrees):
        self.angle = (self.angle - degrees) % 360

    def fire(self):
        self.cannon.fire()

# 대포 클래스 정의
class Cannon(Ship):
    def __init__(self):
        super().__init__()

        # 함포 색깔, 위치 설정
        self.cannon_color = self.color
        self.cannon_position = self.position
        self.cannon_x = self.position[0]
        self.cannon_y = self.position[1]
        self.cannon_angle = 0

        # 대포알 색깔, 위치, 속력 등 설정
        self.cannonball_color = self.cannon_color
        self.cannonball_position = self.cannon_position
        self.cannonball_x = self.cannon_x
        self.cannonball_y = self.cannon_y
        self.cannonball_angle = self.cannon_angle
        self.cannonball_speed = 10
        self.cannonball_radius = 2
        self.cannonball_fired = False
        self.cannonball_hit = False

        # 폰트 설정
        self.font = pygame.font.Font(None, 15)
        self.hit_text = self.font.render("hit", True, ORANGE, WHITE)
        self.miss_text = self.font.render("miss", True, ORANGE, WHITE)

# 아래서부터 다시 생각해 보자~~~~~~~~~~~~₩
    
    def move_cannonball(self):
        pygame.draw.circle(self.screen, self.cannonball_color, self.cannonball_position, self.cannonball_radius)

        if self.cannonball_fired:

            self.cannonball_x += self.cannonball_speed * math.sin(math.radians(self.cannonball_angle))
            self.cannonball_y -= self.cannonball_speed * math.cos(math.radians(self.cannonball_angle))
            pygame.draw.circle(self.screen, self.cannonball_color, (self.cannonball_x, self.cannonball_y), self.cannonball_radius)

            if (not self.color != self.cannonball_color) or (not WHITE != self.cannonball_color):
                self.cannonball_hit = True
                self.cannonball_fired = False
                self.screen.blit(self.hit_text, (self.target_x - 20, self.target_y - 20))


            # 자기 색깔이 아닌 것이 맞았을 경우
            if (not self.target_hit) and abs(self.cannonball_x - self.target_x) < 30 and abs(self.cannonball_y - self.target_y) < 30 and self.target_color != (0, 0, 255):
                self.target_hit = True
                self.cannonball_fired = False
                self.cannonball_color = (255, 0, 0)
                hit_text = self.font.render("hit", True, (255, 165, 0), (255, 255, 255))
                self.screen.blit(hit_text, (self.target_x - 20, self.target_y - 20))
            elif self.cannonball_y < 0 or self.cannonball_x < 0 or self.cannonball_x > self.width:
                self.cannonball_fired = False
                miss_text = self.font.render("miss", True, (255, 165, 0), (255, 255, 255))
                self.screen.blit(miss_text, (self.cannonball_x - 20, self.cannonball_y - 20))
'''
    # 대포와 전투함 간 충돌 여부 확인
    def check_collision(self, target):
        return self.rect.colliderect(target.rect)

    def fire(self):
        return
'''

# Q-learning 알고리즘을 위한 클래스 정의
class QLearning:
    def __init__(self, num_states, num_actions, alpha=0.5, alpha_min=0.1, alpha_decay=0.9999,
                 gamma=0.99, epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.9999):
        self.alpha = alpha
        self.alpha_min = alpha_min
        self.alpha_decay = alpha_decay
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.num_states = num_states
        self.num_actions = num_actions
        self.q_table = np.zeros((self.num_states, self.num_actions))
        self.num_steps = 0
        self.total_reward = 0.0

    def get_action(self, state):
        if np.random.rand() < self.epsilon:  # epsilon-greedy 방법으로 행동 선택
            return np.random.randint(self.num_actions)
        else:
            return np.argmax(self.q_table[state])

    def update_table(self, state, action, reward, next_state):
        q_1 = self.q_table[state, action]
        q_2 = reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state, action] += self.alpha * (q_2 - q_1)
        self.alpha = max(self.alpha * self.alpha_decay, self.alpha_min)
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
        self.num_steps += 1
        self.total_reward += reward

# 학습을 위한 변수
state_size = 800
action_size = 3
q_learning = QLearning(state_size, action_size, alpha=0.2, gamma=0.95)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battleship Game with Q-function")
    clock = pygame.time.Clock()

    # 전투함 생성
    blue_1 = Ship(screen, BLUE, (300, 500))
    red_1 = Ship(screen, RED, (300, 100))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(blue_1, red_1)

    # Q-Learning 알고리즘을 사용한 강화학습 객체 생성
    q_learning = QLearning(num_states=8000, num_actions=3, gamma=0.95)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 상태(state)와 행동(action) 설정
        # state = (blue_1의 x좌표, blue_1의 y좌표, red_1의 x좌표, red_1의 y좌표)로 정의
        blue_1_x = blue_1.rect.x // 100
        blue_1_y = blue_1.rect.y // 100
        red_1_x = red_1.rect.x // 100
        red_1_y = red_1.rect.y // 100
        state = blue_1_x * 1000 + blue_1_y * 100 + red_1_x * 10 + red_1_y

        # 행동 선택
        action = q_learning.get_action(state)

        # 행동 실행
        if action == 0:
            blue_1.rect.y -= 10
        elif action == 1:
            blue_1.rect.y += 10
        else:
            pass

        # 전투함 상호작용
        hit_blue = False
        hit_red = False
        if red_1.can_shoot:
            hit_blue = red_1.shoot(blue_1)
            if hit_blue:
                red_1.can_shoot = False
                # red_1이 blue_1을 맞추면 점수 +1
                reward = 1
                print("Red_1 hit Blue_1. +1 point")
        if blue_1.can_shoot:
            hit_red = blue_1.shoot(red_1)
            if hit_red:
                # blue_1이 red_1을 맞추면 게임 종료
                reward = -1
                print("Blue_1 hit Red_1. Game over!")
                running = False
            else:
                # blue_1이 먼저 쏘면 점수 -0.5
                if not hit_blue:
                    reward = -0.5
                    print("Blue_1 shot first. -0.5 points")
                blue_1.can_shoot = False
            if hit_blue:
                # blue_1이 맞았다면 점수 -1
                reward = -1
                print("Blue_1 got hit. -1 point")

        # 학습
        next_blue_1_x = blue_1.rect.x // 100
        next_blue_1_y = blue_1.rect.y // 100
        next_state = next_blue_1_x * 1000 + next_blue_1_y * 100 + red_1_x * 10 + red_1_y
        q_learning.update_table(state, action, reward, next_state)

        # 화면 갱신
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()

        # 다음 스텝으로
        q_learning.num_steps += 1
        q_learning.total_reward += reward

        # 다음 state, epsilon, alpha 계산
        state = next_state
        q_learning.epsilon = max(q_learning.epsilon * q_learning.epsilon_decay, q_learning.epsilon_min)
        q_learning.alpha = max(q_learning.alpha * q_learning.alpha_decay, q_learning.alpha_min)

    pygame.quit()

if __name__ == "__main__":
    main()