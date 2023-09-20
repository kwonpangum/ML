import pygame
import random
import math
import matplotlib.pyplot as plt

pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 폰트
font = pygame.font.Font(None, 15)

# 대포 발사 클래스
class Projectile:
    def __init__(self, x, y, color, target_pos):
        self.pos = [x, y]
        self.color = color
        self.target_pos = target_pos
        self.speed = 5
        self.radius = 5

    def move(self):
        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            self.pos[0] += self.speed * dx / distance
            self.pos[1] += self.speed * dy / distance

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

    def check_collision(self, target_ship):
        dx = self.pos[0] - target_ship.pos[0]
        dy = self.pos[1] - target_ship.pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance <= self.radius + target_ship.radius:
            return True
        return False

# Ship 클래스 만들기
class Ship:
    def __init__(self, x, y, color, health, max_speed):
        self.pos = [x, y]
        self.color = color
        self.health = health
        self.max_speed = max_speed
        self.radius = 5
        self.cannon_range = 500 if color == BLUE else 450
        self.movement = {
            "up": [0, -1],
            "down": [0, 1],
            "left": [-1, 0],
            "right": [1, 0],
        }

    def move(self, direction):
        if direction in self.movement:
            move_x, move_y = self.movement[direction]
            self.pos[0] += move_x * self.max_speed
            self.pos[1] += move_y * self.max_speed

            # Keep the ship inside the screen
            self.pos[0] = max(self.radius, min(WIDTH - self.radius, self.pos[0]))
            self.pos[1] = max(self.radius, min(HEIGHT - self.radius, self.pos[1]))

    def fire(self, target_ship):
        projectile = Projectile(self.pos[0], self.pos[1], self.color, target_ship.pos)
        return projectile

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)

    def get_state(self):
        return tuple(self.pos + [self.health])

# Ships
blue_1 = Ship(150, 100, BLUE, 1, 3)
red_1 = Ship(150, 200, RED, 1, 2)

# Cannon ranges
blue_cannon_range = 150
red_cannon_range = 130

class Blue1Agent:
    def __init__(self, ship, learning_rate=0.1, discount_factor=0.99, epsilon=0.1):
        self.ship = ship
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = {}
        self.actions = list(self.ship.movement.keys()) + ["fire"]

    def get_state(self):
        return tuple(self.ship.pos)

    def policy(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = [self.q_value(state, action) for action in self.actions]
            return self.actions[q_values.index(max(q_values))]

    def q_value(self, state, action):
        return self.q_table.get((state, action), 0)

    def update_q_table(self, history):
        for state, action, next_state, reward in reversed(history):
            q_old = self.q_value(state, action)
            max_q_next_state = max([self.q_value(next_state, a) for a in self.actions])
            self.q_table[(state, action)] = q_old + self.learning_rate * (reward + self.discount_factor * max_q_next_state - q_old)

blue_1_agent = Blue1Agent(blue_1)

def main(num_episodes=10000):
    episode_rewards = []
    projectiles = []
    actions = ["up", "down", "left", "right", "fire"]

    def draw_middle_line(surface, color):
        pygame.draw.line(surface, color, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)

    # The perform_action function implementation
    def perform_action(ship, target_ship, action):
        projectile = None
        if action in ship.movement:
            ship.move(action)
        elif action == "fire":
            projectile = ship.fire(target_ship)

        next_state = ship.get_state()

        # Calculate the reward
        reward = 0
        if target_ship.health <= 0:
            reward += 1
        if ship.health <= 0:
            reward -= 1
        if ship.pos[1] < HEIGHT // 2:
            reward -= 0.1
        reward -= 0.001  # Penalty for each movement

        return next_state, reward, projectile

    for episode in range(num_episodes):

        # Reset ships' health and positions for each episode
        blue_1.health = 1
        blue_1.pos = [150, 200]
        red_1.health = 1
        red_1.pos = [150, 100]

        running = True
        total_moves = 0
        total_reward = 0
        episode_history = []

        while running:
            # ... (All previous code inside the main loop)
            # Fill the screen with the background color
            screen.fill(WHITE)
            draw_middle_line(screen, RED)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Agent's action
            state = blue_1_agent.get_state()
            action = blue_1_agent.policy(state)
            next_state, reward, new_projectile = perform_action(blue_1, red_1, action)
            if new_projectile:
                projectiles.append(new_projectile)

            # Update total reward
            total_reward += reward

            # Save action and reward to history
            episode_history.append((state, action, next_state, reward))

            # Red ship's random action
            red_action = random.choice(actions)
            red_next_state, _, red_new_projectile = perform_action(red_1, blue_1, red_action)
            if red_new_projectile:
                projectiles.append(red_new_projectile)

            # Check the termination conditions
            if blue_1.health <= 0 or red_1.health <= 0:
                running = False

            # Update and draw projectiles
            for projectile in projectiles[:]:
                projectile.move()
                projectile.draw(screen)

                if projectile.check_collision(blue_1) or projectile.check_collision(red_1):
                    projectiles.remove(projectile)
                    if projectile.color == BLUE:
                        red_1.health -= 1
                    elif projectile.color == RED:
                        blue_1.health -= 1

                # Remove projectiles that are off the screen
                if projectile.pos[0] < 0 or projectile.pos[0] > WIDTH or projectile.pos[1] < 0 or projectile.pos[1] > HEIGHT:
                    projectiles.remove(projectile)

            # Update the screen
            blue_1.draw(screen)
            red_1.draw(screen)
            pygame.display.flip()
            pygame.time.delay(50)
            # Update the window title with the current episode number
            pygame.display.set_caption(f"전투함 시뮬레이션_PK - Episode: {episode + 1}")

            # Draw episode number
            episode_text = font.render(f"Episode: {episode + 1}", True, (0, 0, 0))
            screen.blit(episode_text, (10, 10))

            # Update total reward
            total_reward += reward

            if blue_1.health <= 0 or red_1.health <= 0:
                running = False

        # Update Q-table using episode history
        blue_1_agent.update_q_table(episode_history)

        # Save total reward for this episode
        episode_rewards.append(total_reward)

    # Plot episode rewards
    plt.plot(episode_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Total Reward per Episode")
    plt.show()

if __name__ == "__main__":
    main()
