import random 
import numpy as np

N = 10000
Z_plus = np.array([1, 0])
Z_minus = np.array([0, 1])

def measure_z_Pauli(state):
    p_up = np.abs(np.vdot(Z_plus, state))**2
    if random.random() < p_up:
        return Z_plus, "up"
    else:
        return Z_minus, "down"
    
particles = [random.choice([Z_plus, Z_minus]) for i in range(N)]

collapsed = [measure_z_Pauli(p)[0] for p in particles]
labels_first = [measure_z_Pauli(p)[1] for p in particles]

collapsed_pairs = [measure_z_Pauli(p) for p in particles]
collapsed_states = [s for s , lbl in collapsed_pairs]
labels_first = [lbl for s, lbl in collapsed_pairs]

Z_plus_survivours = [s for s, lbl in collapsed_pairs if lbl == "up"]
print("First measurement gave", len(Z_plus_survivours), "Z+ survivors (≈ N/2)")

results_second = [measure_z_Pauli(s)[1] for s in Z_plus_survivours]
print("Second measurement on survivors:", results_second.count("up"), "Z+", results_second.count("down"), "Z-")