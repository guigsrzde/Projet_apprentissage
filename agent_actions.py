import pandas as pd
import matplotlib.pyplot as plt
from gamedata import GameData

def draw_graphs_model(csv_path: str):
    # Load CSV data
    data = pd.read_csv(csv_path)
    city_ids = list(data["City id"].unique())

    # Set up plot grid
    n = len(city_ids)
    nrows = int((n + 1) ** 0.5)
    ncols = nrows
    while nrows * ncols < n + 1:  # +1 for mutation plot
        ncols += 1

    fig, ax = plt.subplots(nrows, ncols,figsize=(20, 30),squeeze=False,gridspec_kw={'hspace': 0.6, 'wspace': 0.4})

    # Plot infection stats for each city
    for k in range(n):
        city_data = data[data["City id"] == city_ids[k]]
        row, col = k // ncols, k % ncols
        
        if k == 0:

            ax[row][col].plot(city_data["Healthy"], label='healthy')
            ax[row][col].plot(city_data["Infected"], label='infected')
            ax[row][col].plot(city_data["Recovered"], label='recovered')
            ax[row][col].plot(city_data["Dead"], label='dead')
            ax[row][col].legend(fontsize='x-small')
        
        else:
            ax[row][col].plot(city_data["Healthy"])
            ax[row][col].plot(city_data["Infected"])
            ax[row][col].plot(city_data["Recovered"])
            ax[row][col].plot(city_data["Dead"])


        ax[row][col].set_title(f"City ID: {city_ids[k]}")
        ax[row][col].grid()

    # Mutation points plot
    row, col = n // ncols, n % ncols
    city0_data = data[data["City id"] == city_ids[0]]
    maxturns = len(city0_data)
    game = GameData("royaume_uni", maxturns)

    # Load mutation costs
    symptom_costs = {name: sym.mutation_cost for name, sym in game.virus.symptoms.items()}

    # Mutation point tracking
    mutation_points_after = [game.virus.mutation_points]
    mutation_points_before = [game.virus.mutation_points]
    actions = city0_data["Actions"].tolist()

    # Ensure actions are parsed if stored as strings
    import ast
    actions = [ast.literal_eval(a) if isinstance(a, str) else a for a in actions]

    for i in range(maxturns - 1):
        new_value = mutation_points_after[-1]
        mutation_points_before.append(new_value+2)
        if i!=0:
            new_value+=2
        for action in actions[i]:
            new_value -= symptom_costs.get(action, 0)
        mutation_points_after.append(new_value)

    ax[row][col].plot(mutation_points_after, label='after spending')
    ax[row][col].scatter(range(maxturns), mutation_points_before, label='before spending')
    for name, cost in symptom_costs.items():
        ax[row][col].axhline(y=cost, color='red', linestyle='--', linewidth=1, label=f"{name} ({cost})")

    ax[row][col].legend(fontsize='x-small')
    ax[row][col].set_title("Use of Mutation Points")
    ax[row][col].grid()

    # Turn off unused subplots
    for k in range(n + 1, nrows * ncols):
        row, col = k // ncols, k % ncols
        ax[row][col].axis('off')
    plt.tight_layout()
    plt.show()


draw_graphs_model("test_2")

