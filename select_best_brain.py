import pickle
from run_dpl import plot_results, validate_brain

with open('brains.pkl', 'rb') as f:
    data = pickle.load(f) #[(vax_t, scores, brains)]

best_brain_id = 0
best_brain_avg = [0 for _ in range(5,19)]
best_vax = []
best_scores = []
for i in range(len(data)):
    print(f"brain number {i+1}")
    vax, scores = validate_brain(data[i], 20)
    avg = [0 for _ in range(5,19)]
    n = [0 for _ in range(5,19)]
    for j in range(len(vax)):
        avg[vax[j]-5] += scores[j]
        n[vax[j]-5] += scores[j]
    for k in range(len(avg)):
        if n[k]==0:
            avg[k] == 0
        else:
            avg[k] /= n[k]
    if sum(avg) > sum(best_brain_avg) and min([avg[l] - best_brain_avg[l] for l in range(len(avg))]) > -4:
        best_brain_id = i
        best_brain_avg = avg
        best_vax = vax
        best_scores = scores
        best_brain_avg = avg

plot_results(best_vax, best_scores)


