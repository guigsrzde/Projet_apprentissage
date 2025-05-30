import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
from plague_inc_env import PlagueIncEnv
import gymnasium as gym

# Définition du réseau de neurones
class DQN(nn.Module):
    def __init__(self, input_shape, num_actions):
        super(DQN, self).__init__()
        
        # Calculer la taille d'entrée aplatie (num_cities * 4)
        flat_size = input_shape[0] * input_shape[1]
        
        # Réseau simple
        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(flat_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_actions)
        )
    
    def forward(self, x):
        return self.network(x)
    


#########################################

class DQNAgent:
    def __init__(self, state_shape, num_actions, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.state_shape = state_shape
        self.num_actions = num_actions
        self.gamma = gamma  # Facteur de décompte pour les récompenses futures
        self.epsilon = epsilon  # Pour l'exploration
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.memory = deque(maxlen=10000)  # Mémoire de replay
        
        # Réseaux de neurones principal et cible
        self.model = DQN(state_shape, num_actions)
        self.target_model = DQN(state_shape, num_actions)
        self.update_target_model()
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()
        
    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.num_actions)
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Ajout d'une dimension batch
        q_values = self.model(state_tensor)
        return torch.argmax(q_values).item()
    
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
            
            target = reward
            if not done:
                target += self.gamma * torch.max(self.target_model(next_state_tensor)).item()
            
            q_values = self.model(state_tensor)
            target_f = q_values.clone().detach()
            target_f[0][action] = target
            
            self.optimizer.zero_grad()
            loss = self.loss_fn(q_values, target_f)
            loss.backward()
            self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


#################################################

def train_agent(env_name="PlagueInc-v0", episodes=1000, batch_size=32):
    env = gym.make(env_name)  
    total_actions = sum(env.action_space.nvec)
    agent = DQNAgent(
        state_shape=env.observation_space.shape,
        num_actions=total_actions,
    )
    
    scores = []
    
    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        score = 0
        
        while not done:
            # Sélectionner une action
            action = agent.act(state)
            
            # Exécuter l'action
            next_state, reward, done, _, _ = env.step(action)
            
            # Mémoriser l'expérience
            agent.remember(state, action, reward, next_state, done)
            
            # Mettre à jour l'état courant
            state = next_state
            
            # Accumuler la récompense
            score += reward
            
            # Entraîner sur un batch aléatoire
            agent.replay(batch_size)
        
        scores.append(score)
        
        # Mettre à jour le modèle cible après chaque épisode
        if episode % 10 == 0:
            agent.update_target_model()
            
        print(f"Episode {episode}, Score: {score}, Epsilon: {agent.epsilon:.4f}")
        
        # Sauvegarder le modèle périodiquement
        if episode % 100 == 0:
            torch.save(agent.model.state_dict(), f"plague_dqn_model_{episode}.pt")
    
    return agent, scores


###################################


if __name__ == "__main__":
    trained_agent, training_scores = train_agent(episodes=500)
    
    # Sauvegarder le modèle final
    torch.save(trained_agent.model.state_dict(), "plague_dqn_final.pt")
    
    # Sauvegarder les scores (optionnel, pour analyse)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.plot(training_scores)
    plt.title('Scores d\'entraînement')
    plt.xlabel('Épisodes')
    plt.ylabel('Score')
    plt.savefig('training_scores.png')
    plt.show()