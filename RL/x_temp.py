import pygame
import numpy as np

# 게임 환경 설정
WIDTH, HEIGHT = 800, 600
FPS = 60

# 전투함 클래스 정의
class Battleship(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.can_shoot = True

    def shoot(self, target):
        if self.can_shoot:
            cannonball = Cannonball(self.rect.x, self.rect.y)
            return cannonball.check_collision(target)
        return False

# 대포 클래스 정의
class Cannonball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # 대포와 전투함 간 충돌 여부 확인
    def check_collision(self, target):
        return self.rect.colliderect(target.rect)

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
    blue_1 = Battleship(50, HEIGHT // 2, (0, 0, 255))
    red_1 = Battleship(WIDTH - 100, HEIGHT // 2, (255, 0, 0))

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