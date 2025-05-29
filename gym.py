from typing import Optional
import numpy as np
import gymnasium as gym

class GymEnv(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Discrete(3) # On a 3 symptomes sur lesquels ont peut jouer


    def _get_obs(self):
        pass

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        pass

    def step(self, action):
        pass

    