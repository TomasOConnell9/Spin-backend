import numpy as np
import random
import tkinter as tk

# Basis states
Z_plus = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)

X_plus = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)

Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)


def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec


def measure_z(state):
    prob_up = np.abs(np.vdot(Z_plus, state))**2
    if random.random() < prob_up:
        return Z_plus, "up"
    else:
        return Z_minus, "down"

def measure_x(state):
    prob_up = np.abs(np.vdot(X_plus, state))**2
    if random.random() < prob_up:
        return X_plus, "up"
    else:
        return X_minus, "down"

def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    if random.random() < prob_up:
        return Y_plus, "up"
    else:
        return Y_minus, "down"


def measure(state, axis):
    """General measurement along chosen axis."""
    if axis == "z":
        return measure_z(state)
    elif axis == "x":
        return measure_x(state)
    elif axis == "y":
        return measure_y(state)
    else:
        raise ValueError("Invalid axis. Choose x, y, or z.")


def run_two_measurements():
    axis1 = axis1_var.get() #Pick what axis for first measurment
    axis2 = axis2_var.get() #Pick second axis
    filter_choice = filter_var.get() #Up or down 
    try:
        N = int(entry_atoms.get()) #Pick how many atoms we want to measure
    except ValueError:
        result_label.config(text="Please enter a valid number of atoms.")
        return

    first_up = 0
    first_down = 0
    second_up = 0
    second_down = 0 #these four set each state measurement to 0

    for i in range(N): #for every index, i, in N we are going to:
        psi = random_state() #generate a random state
        collapsed_state, outcome1 = measure(psi, axis1) #Measure along first axis, collapsed state is now tied to outcome from measurement 1

        if outcome1 == "up":
            first_up += 1
        else:
            first_down += 1

        if outcome1 == filter_choice: #if outcome of axis1 is the same as the filter choice, outcome passes through. Otherwise its blocked. 
            _, outcome2 = measure(collapsed_state, axis2)  # Measure the same atom along the second axis; outcome2 is "up" or "down" based on quantum probabilities
            if outcome2 == "up":
                second_up += 1
            else:
                second_down += 1

    result_label.config(
        text=f"Second measurement ({axis2.upper()})"
             f"\nUp:   {second_up}"
             f"\nDown: {second_down}"
    )


# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("Stern-Gerlach Simulator")

# First axis
axis1_var = tk.StringVar(value="z")
tk.Label(root, text="First analyzer axis:").pack()
tk.OptionMenu(root, axis1_var, "x", "y", "z").pack()

# Filter choice
filter_var = tk.StringVar(value="up")
tk.Label(root, text="Filter outcome from first analyzer:").pack()
tk.OptionMenu(root, filter_var, "up", "down").pack()

# Second axis
axis2_var = tk.StringVar(value="z")
tk.Label(root, text="Second analyzer axis:").pack()
tk.OptionMenu(root, axis2_var, "x", "y", "z").pack()

# Number of atoms
tk.Label(root, text="Number of atoms:").pack()
entry_atoms = tk.Entry(root)
entry_atoms.insert(0, "10000")
entry_atoms.pack()

# Run button
tk.Button(root, text="Run Sequential Measurement", command=run_two_measurements).pack(pady=5)

# Results
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
