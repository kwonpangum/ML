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

# ... (All previous code including Ship, Blue1Agent classes, and helper functions)

def main(num_episodes=100):
    episode_rewards = []

    for episode in range(num_episodes):
        # Reset ships' health and positions for each episode
        blue_1.health = 1
        blue_1.pos = [300, 100]
        red_1.health = 1
        red_1.pos = [300, 500]

        running = True
        total_moves = 0
        total_reward = 0
        episode_history = []

        while running:
            # ... (All previous code inside the main loop)

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
