import numpy as np
import random


Z_plus = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)

X_plus = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)

Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)

def theta_plus(theta):
    return np.array([np.cos(np.radians(theta)/2), np.sin(np.radians(theta)/2)])

def theta_minus(theta):
    return np.array([-np.sin(np.radians(theta)/2), np.cos(np.radians(theta)/2)])


def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec

# Measurement functions
def measure_z(state):
    prob_up = np.abs(np.vdot(Z_plus, state))**2
    prob_down = np.abs(np.vdot(Z_minus, state)) **2
    if  prob_down > random.random():
        return Z_plus, "up"
    else:
        return Z_minus, "down"

def measure_x(state):
    prob_up = np.abs(np.vdot(X_plus, state))**2
    prob_down = np.abs(np.vdot(X_minus, state)) **2
    if prob_down > random.random():
        return X_plus, "up"
    else:
        return X_minus, "down"

def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    prob_down = np.abs(np.vdot(Y_minus, state)) **2
    if prob_down > random.random():
        return Y_plus, "up"
    else:
        return Y_minus, "down"
    
def measure_theta(state, theta):
    T_plus = theta_plus(theta)
    T_minus = theta_minus(theta)
    
    prob_up = np.abs(np.vdot(T_plus, state))**2
    prob_down = np.abs(np.vdot(T_minus, state))**2
    if prob_up > random.random():
        return T_plus, "up"
    else:
        return T_minus, "down"
    



if __name__ == "__main__":
    axis = input("Choose measurement axis (x, y, z, θ): ").strip().lower()
    if axis == "θ":
        theta = int(input("What angle (in degrees): "))
    N = int(input("How many particles? "))
    up_count = 0
    down_count = 0

    for _ in range(N):
        psi = random_state()

        if axis == "z":
            _, outcome = measure_z(psi)
        elif axis == "x":
            _, outcome = measure_x(psi)
        elif axis == "y":
            _, outcome = measure_y(psi)
        else:
            _, outcome = measure_theta(psi, theta)

        if outcome == "up":
            up_count += 1
        else:
            down_count += 1

    print(f"{axis.upper()}-up:   {up_count}")
    print(f"{axis.upper()}-down: {down_count}")


