import torch
import torch.nn as nn
import torch.optim as optim
from gamedata import GameData
import random

episodes = 1000

class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, state):
        return self.network(state)
    
    def train_policy(self):

        optimizer = optim.Adam(self.parameters(), lr=0.001)
        
        for e in episodes:  
            game = GameData("random", 20)
            epoch_data = []
            
            # Play Game
            while game.turn<21:
                # Retrieve state
                current_state = encode_game_state(game)
                
                action_probs = self(torch.FloatTensor(current_state))

                actions = select_actions(current_state, action_probs)
                
                # Execute action in the game
                execute_action(game, actions)
                game.click_turn()  # Takes a step in the simulation
                
                # Calculates the reward
                reward = calculate_reward(game)
                next_state = encode_game_state(game)
                
                # Stocker l'expérience
                epoch_data.append((current_state, actions, reward))
            
            # À la fin de la partie, mettre à jour la politique
            update_policy(optimizer, epoch_data)


    def select_actions(self, state, epsilon):
        
        # Décider d'explorer ou d'exploiter
        if random.random() < epsilon:
            # Exploration: choisir une action aléatoire
            return random.randrange(self.action_space)
        else:
            # Exploitation: choisir la meilleure action selon le modèle
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                q_values = self.policy_net(state_tensor)
                return q_values.max(1)[1].item()  # Indice de la valeur Q maximale


    def update_policy(self, optimizer, epoch_data):
        policy_loss = []
        
        for state, action_idx, reward in epoch_data:
            
            action_probs = self(torch.FloatTensor(state))
            log_prob = torch.log(action_probs[action_idx])
            policy_loss.append(-log_prob * reward) 
        
        optimizer.zero_grad()
        policy_loss = torch.stack(policy_loss).sum()
        policy_loss.backward()
        optimizer.step()
    

def execute_action(game, actions):
    for symptom in actions.values():
        game.click_symptom(symptom.name)
        game.history.add_action(game.turn, symptom.name)


def calculate_reward(game):
    # Récompense basée sur le nombre de personnes tuées ce tour-ci
    current_deaths = sum(town.dead[-1]*town.pop for town in game.towns)
    previous_deaths = sum(town.dead[-2]*town.pop if len(town.deaths)>1 else 0 for town in game.towns)
    new_deaths = current_deaths - previous_deaths
    
    return new_deaths
        

## Permet d'accéder à l'état du jeu sous forme de vecteur

def encode_game_state(game):
    state_vector = []
    for town in game.towns:
        state_vector.extend([
            town.infected[-1],
            town.recovered[-1],
            town.deaths[-1],
            town.vaccination_prop
        ])
    state_vector.extend([
        game.virus.mutation_points,
        game.virus.propagation,
        game.virus.mortality_symptoms,
        game.virus.infection_duration
    ])
    return torch.FloatTensor(state_vector)

