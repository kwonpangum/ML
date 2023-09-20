# AI_BattleShip_Agent

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


def main():
    running = True
    episode_history = []

    while running:
        # ...

        # Implement your reinforcement learning algorithm here
        # Example: Use e-greedy policy from Blue1Agent
        state = blue_1_agent.get_state()
        action = blue_1_agent.policy(state)

        if action == "fire":
            blue_1.fire(red_1)
        else:
            blue_1.move(action)

        total_moves += 1

        # ...

        # Get reward and next_state
        next_state = tuple(blue_1.pos)
        reward = get_reward(blue_1, red_1, total_moves, red_1_fired, blue_1_fired_before_red)

        episode_history.append((state, action, next_state, reward))

        if blue_1.health <= 0 or red_1.health <= 0:
            running = False

    # Update Q-table using episode history
    blue_1_agent.update_q_table(episode_history)

    pygame.quit()


if __name__ == "__main__":
    main()


