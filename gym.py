import gymnasium as gym
from gymnasium import spaces
import numpy as np
from gamedata import GameData

class PlagueIncEnv(gym.Env):
    """
    Environnement Gym pour le jeu PlagueInc
    """
    
    metadata = {'render.modes': ['human', 'rgb_array']}
    
    def __init__(self, map):
        super(PlagueIncEnv, self).__init__()
        
        # Initialisation du jeu 
        self.game = self.initialize_game()
        self.map_name = map
        
        # Définition de l'esapce d'actions
        self.action_space = self._define_action_space()
        
        # Définition de l'espace d'observations
        self.observation_space = self._define_observation_space()
        
        # État actuel du jeu
        self.state = None
        self.steps = 0
        
    def initialize_game(self):
        """
        Initialise le jeu avec le constructeur de GameData et la map en argument
        """
        game = GameData(self.map_name, 20)
        return game
    
    def _define_action_space(self):
        """
        Défini l'espace des actions, ici ce sont les différents symptômes
        """
        action_space = {}
        for symptom in self.game.virus.symptoms.keys():
            action_space[symptom] = 0 # On initialise toutes les actions à 0
        return action_space
    
    def _define_observation_space(self):
        """
        Définit l'espace d'observation avec une structure plus organisée.
        """
        num_cities = len(self.game.cities)
        
        return spaces.Dict({
            "cities": spaces.Tuple([
                spaces.Dict({
                    "infected": spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                    "healthy": spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                    "dead": spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                    "recovered": spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
                }) for _ in range(num_cities)
            ])
        })
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Réinitialise le jeu
        self.initialize_game()
        self.steps = 0
        
        # Calculee l'état initial
        self.state = self._get_observation()
        return self.state, {}
    
    def step(self, action):
        """
        Simule une étape en appelant les actions et simulant click_turn()
        """

        # Appliquer l'action
        self._apply_action(action)

        # Mettre à jour toutes les grandeurs
        self.game.click_turn()
        
        # Mettre à jour l'état
        self.state = self._get_observation()
        
        # Calculer la récompense
        reward = self._calculate_reward()
        
        # Vérifier si l'épisode est terminé
        done = self._is_done()
        
        self.steps += 1
        
        return self.state, reward, done, False, {}
    
    def _apply_action(self, action):
        """
        Convertit les actions en équivalent de click_symptom()
        """
        for symptom in action: # On parcourt le dictionnaire des actions
            for i in range (action[symptom]): # On récupère le nombre de fois qu'on veut réaliser chaque action
                self.game.click_symptom(symptom) # On utilise click_symptom() pour appliquer l'action
    
    
    def _get_observation(self):
        """
        Convertit l'état actuel du jeu en une observation structurée.
        """
        return {
            "cities": tuple({
                "infected": np.array([city.infected[-1]], dtype=np.float32),
                "healthy": np.array([city.healthy[-1]], dtype=np.float32),
                "dead": np.array([city.dead[-1]], dtype=np.float32),
                "recovered": np.array([city.recovered[-1]], dtype=np.float32),
            } for city in self.game.cities)
        }
    
    def _calculate_reward(self):
        return self.game.score_function1()
    
    def _is_done(self):
        """
        Détermine si l'épisode est terminé
        """
        if self.game.turn < 21:
            return False
        else:
            return True
        
    
    def render(self):
        # Rendu graphique (optionnel)
        pass
    
    def close(self):
        # Nettoyer les ressources (optionnel)
        pass
