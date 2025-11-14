import numpy as np 
import random

Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)


def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec

def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    prob_down = np.abs(np.vdot(Y_minus, state))**2
    
    #print(f" Probabilities: Up = {prob_up:.2f}, Down = {prob_down:.2f}, Total = {prob_up+prob_down:.2f}")
    
    if prob_up > prob_down:
        return Y_plus, "up"
    else:
        return Y_minus, "down"
    

N = 10000
up_count = 0
down_count = 0
for i in range(N):
    psi = random_state()
    a = psi[0]
    b = psi[1]
    
    #print(f"||ψ⟩ = ({a:.2f})|1⟩ + ({b:.2f})|2⟩")
    
    _, outcome = measure_y(psi)
    #print("Measurement result: ", outcome)
    if outcome == "up":
        up_count += 1
    else:
        down_count += 1
        
print("Y-up: ", up_count)
print("Y-down: ", down_count)