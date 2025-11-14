import numpy as np
import random

import numpy as np

Z_plus  = np.array([1, 0, 0], dtype=complex)
Z_zero  = np.array([0, 1, 0], dtype=complex)
Z_minus = np.array([0, 0, 1], dtype=complex)

X_plus  = (1/2) * np.array([1,  np.sqrt(2),  1], dtype=complex)
X_zero  = (1/np.sqrt(2)) * np.array([-1, 0, 1], dtype=complex)
X_minus = (1/2) * np.array([1, -np.sqrt(2),  1], dtype=complex)

Y_plus  = (1/2) * np.array([-1, -1j*np.sqrt(2),  1], dtype=complex)
Y_zero  = (1/np.sqrt(2)) * np.array([1, 0, 1], dtype=complex)
Y_minus = (1/2) * np.array([-1,  1j*np.sqrt(2),  1], dtype=complex)


def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    c = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b, c], dtype = complex)
    vec /= np.linalg.norm(vec)
    
    return vec

def manual_input():
    # safe parser that accepts sqrt, pi, e, i, etc.
    def parse(val):
        env = {
            "__builtins__": None,  # block dangerous builtins
            "np": np,
            "sqrt": np.sqrt,
            "pi": np.pi,
            "e": np.e,
            "i": 1j,
            "^": np.square
        }
        try:
            return complex(eval(val, env))
        except Exception:
            return complex(float(val))

    print("\nEnter amplitudes (you can use sqrt, pi, e, i, etc.)")
    a = parse(input("a|: "))
    b = parse(input("b|: "))
    c = parse(input("c|: "))
    vec = np.array([a, b, c], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec



def measure_z(state):
    prob_up = np.abs(np.vdot(Z_plus, state))**2
    prob_zero = np.abs(np.vdot(Z_zero, state))**2
    prob_down = np.abs(np.vdot(Z_minus, state))**2
    random_num = random.random()
    
    if prob_up > random_num:
        return Z_plus, "up"
    elif prob_zero + prob_up > random_num:
        return Z_zero, "zero"
    else:
        return Z_minus, "down"

def measure_x(state):
    prob_up = np.abs(np.vdot(X_plus, state))**2
    prob_zero = np.abs(np.vdot(X_zero, state))**2
    random_num = random.random()
    
    if prob_up > random_num:
        return X_plus, 'up'
    if prob_up  + prob_zero > random_num:
        return Z_zero, "zero"
    else:
        return X_minus, "down"


def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    prob_zero = np.abs(np.vdot(Y_zero, state))**2
    random_num = random.random()
    
    if prob_up > random_num:
        return Y_plus, 'up'
    if prob_up  + prob_zero > random_num:
        return Y_zero, "zero"
    else:
        return Y_minus, "down"


if __name__ == "__main__":
    up_count = 0
    zero_count = 0
    down_count = 0
    axis = input("What axis (x, y, z): ")
    input_type = input("Random input(y/n)? ")
    N = int(input("How many atoms? "))
    manual = manual_input()
    
    for _ in range(N):
        if input_type == "y":
            
            psi = random_state()

            if axis == "z":
                _, outcome = measure_z(psi)
            elif axis == "x":
                _, outcome = measure_x(psi)
            else:
                _, outcome = measure_y(psi)


            if outcome == "up":
                up_count += 1
            elif outcome == "zero":
                zero_count += 1
            else:
                down_count += 1
        else:
            
            psi = manual
            
            if axis == "z":
                _, outcome = measure_z(psi)
            elif axis == "x":
                _, outcome = measure_x(psi)
            else:
                _, outcome = measure_y(psi)


            if outcome == "up":
                up_count += 1
            elif outcome == "zero":
                zero_count += 1
            else:
                down_count += 1
            
    print(f"Z up: {up_count}")
    print(f"Z zero: {zero_count}")
    print(f"Z down: {down_count}")
    