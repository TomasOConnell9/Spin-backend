import random 
import numpy as np


def measure(prob_up):
    return "up" if random.random() < prob_up else "down"

N = 10000

z_measurements = [measure(0.5) for i in range(N)]
z_plus_counter = z_measurements.count("up")
z_minus_counter = z_measurements.count("down")
print(f"Z+ = {z_plus_counter}, Z- = {z_minus_counter}")



#Using Pauli matrices to find Z+ or Z-
Z_plus = np.array([1, 0])
Z_minus = np.array([0, 1])

sigma_z = np.array([[1, 0],
                   [0, -1]])

def measure_z_Pauli(state):
    p_up = np.abs(np.vdot(Z_plus, state))**2
    if random.random() < p_up:
        return Z_plus, "up"
    else:
        return Z_minus, "down"
    
atoms = [random.choice([Z_plus, Z_minus]) for i in range(N)]
resultsZ = [measure_z_Pauli(p)[1] for p in atoms]
print(resultsZ.count("up"), "Z+", resultsZ.count("down"), "Z-")

#Using Paul martrices to find Y+ or Y-
Y_plus = (1/np.sqrt(2)) * np.array([1, 1j])
Y_minus = (1/np.sqrt(2)) *  np.array([1, -1j])

def measure_y_Pauli(state):
    py_up = np.abs(np.vdot(Y_plus, state))**2 
    if random.random() < py_up:
        return Y_plus, "up"
    else:
        return Y_minus, "down"
    
atomsY = [random.choice([Y_plus, Y_minus]) for i in range(N)]
resultsY = [measure_y_Pauli(p)[1] for p in atomsY]
print(resultsY.count("up"), "Y+", resultsY.count('down'), "Y-")



X_plus = (1/np.sqrt(2)) * np.array([1, 1])
X_minus = (1/np.sqrt(2)) * np.array([1, -1])

def measure_x_Pauli(state):
    px_up = np.abs(np.vdot(X_plus, state))**2
    if random.random() < px_up:
        return X_plus, "up"
    else:
        return X_minus, "down"

atomsX = [random.choice([X_plus, X_minus]) for i in range(N)]
resultsX = [measure_x_Pauli(p)[1] for p in atomsX]
print(resultsX.count("up"), "X+", resultsX.count("down"), "X-")


