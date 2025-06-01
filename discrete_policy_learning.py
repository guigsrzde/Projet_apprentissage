import numpy as np
import numpy.random as rnd
from collections import defaultdict

def reachable_state(turn, S, action=0):
    a=0
    if action == 0:
        a=2
    else:
        a = -1*S[action-1].mutation_cost
    return 30+turn*2-S[1].mutation_cost*(S[1].level+1)-S[2].mutation_cost*(S[2].level+1)-S[0].mutation_cost*(S[0].level+1)+a>=0

class QLearningBrain:
    def __init__(self, symptom_dict, reward_fn, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.995):
        self.symptom_dict = symptom_dict
        self.symptom_list = list(symptom_dict.values())
        self.actions = list(range(len(self.symptom_list) + 1))  # 0 = NULL
        self.q_table = defaultdict(lambda: np.zeros(len(self.actions)))

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

        self.prev_state = None
        self.prev_action = None

        self.reward_fn = reward_fn

    def get_state(self, game):
        levels = tuple(s.level for s in self.symptom_list)
        return (game.turn,) + levels

    def choose_first_city_idx(self, game):
        #return rnd.randint(0, game.ncities)
        return 0

    def choose_action(self, game):
        state = self.get_state(game)

        if state not in self.q_table:
            action = 0

        if rnd.rand() < self.epsilon:
            while True:
                action = rnd.randint(0,4)
                if reachable_state(game.turn, self.symptom_list, int(action)):
                    break
        else:
            action = int(np.argmax(self.q_table[state]))

        self.prev_state = state
        self.prev_action = action

        if action == 0:
            return {}
        else:
            return {action: self.symptom_list[action - 1]}

    def learn(self, game, actions):
        if self.epsilon==0:
            return
        next_state = self.get_state(game)
        reward = self.reward_fn(game, actions)
        done = game.turn >= game.maxturns-1

        current_q = self.q_table[self.prev_state][self.prev_action]
        max_future_q = 0 if done else np.max(self.q_table[next_state])
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[self.prev_state][self.prev_action] = new_q

        if done:
            self.epsilon *= self.epsilon_decay
