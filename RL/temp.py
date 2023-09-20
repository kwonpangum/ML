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
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Ship 클래스 만들기
class Ship:
    def __init__(self, x, y, color, health, max_speed):
        self.pos = [x, y]
        self.color = color
        self.health = health
        self.max_speed = max_speed
        self.radius = 15
        self.cannon_range = 150 if color == BLUE else 130
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
        distance = math.sqrt((self.pos[0] - target_ship.pos[0]) ** 2 + (self.pos[1] - target_ship.pos[1]) ** 2)
        if distance <= self.cannon_range:
            target_ship.health -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)

    def get_state(self):
        return tuple(self.pos + [self.health])

# Ships
blue_1 = Ship(300, 100, BLUE, 1, 3)
red_1 = Ship(300, 500, RED, 1, 2)

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

def main(num_episodes=1000):
    episode_rewards = []

    def draw_middle_line(surface, color):
        pygame.draw.line(surface, color, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)

    # The perform_action function implementation
    def perform_action(ship, target_ship, action):
        if action in ship.movement:
            ship.move(action)
        elif action == "fire":
            ship.fire(target_ship)

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

        return next_state, reward

    for episode in range(num_episodes):
# ---------
        # Reset ships' health and positions for each episode
        blue_1.health = 1
        blue_1.pos = [300, 500]
        red_1.health = 1
        red_1.pos = [300, 100]

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
            next_state, reward = perform_action(blue_1, red_1, action)

            # Update total reward
            total_reward += reward

            # Save action and reward to history
            episode_history.append((state, action, next_state, reward))

            # Red ship's random action
            red_action = random.choice(list(red_1.movement.keys()) + ["fire"])
            _ = perform_action(red_1, blue_1, red_action)

            # Check the termination conditions
            if blue_1.health <= 0 or red_1.health <= 0:
                running = False

            # Update the screen
            blue_1.draw(screen)
            red_1.draw(screen)
            pygame.display.flip()
            pygame.time.delay(50)
# -----
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
