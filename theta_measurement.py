import numpy as np
import random
import tkinter as tk

# --- Basis states ---
Z_plus = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)

X_plus = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)

Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)

def theta_plus(theta):
    """Eigenstate along theta in x-z plane"""
    return np.array([np.cos(np.radians(theta)/2), np.sin(np.radians(theta)/2)], dtype=complex)

def theta_minus(theta):
    """Orthogonal state to theta_plus"""
    return np.array([-np.sin(np.radians(theta)/2), np.cos(np.radians(theta)/2)], dtype=complex)


def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec


def measure_axis(state, axis, theta=None):
    """Measure spin along chosen axis (x, y, z, or theta)."""
    if axis == "z":
        prob_up = np.abs(np.vdot(Z_plus, state))**2
        return (Z_plus, "up") if random.random() < prob_up else (Z_minus, "down")
    elif axis == "x":
        prob_up = np.abs(np.vdot(X_plus, state))**2
        return (X_plus, "up") if random.random() < prob_up else (X_minus, "down")
    elif axis == "y":
        prob_up = np.abs(np.vdot(Y_plus, state))**2
        return (Y_plus, "up") if random.random() < prob_up else (Y_minus, "down")
    elif axis == "θ":
        if theta is None:
            raise ValueError("Theta value must be provided for axis 'θ'.")
        T_plus = theta_plus(theta)
        T_minus = theta_minus(theta)
        prob_up = np.abs(np.vdot(T_plus, state))**2
        return (T_plus, "up") if random.random() < prob_up else (T_minus, "down")
    else:
        raise ValueError("Invalid axis. Choose x, y, z, or θ.")

def run_two_measurements():
    axis1 = axis1_var.get()
    axis2 = axis2_var.get()
    filter_choice = filter_var.get()
    try:
        N = int(entry_atoms.get())
    except ValueError:
        result_label.config(text="Please enter a valid number of atoms.")
        return

    theta1 = int(entry_theta1.get()) if axis1 == "θ" else None
    theta2 = int(entry_theta2.get()) if axis2 == "θ" else None

    first_up = first_down = second_up = second_down = 0

    for _ in range(N):
        psi = random_state()
        collapsed_state, outcome1 = measure_axis(psi, axis1, theta1)

        if outcome1 == "up":
            first_up += 1
        else:
            first_down += 1

        if outcome1 == filter_choice:
            _, outcome2 = measure_axis(collapsed_state, axis2, theta2)
            if outcome2 == "up":
                second_up += 1
            else:
                second_down += 1

    result_label.config(
        text=f"Second measurement ({axis2.upper()})\n"
             f"Up:   {second_up}\n"
             f"Down: {second_down}"
    )

# --- GUI setup ---
root = tk.Tk()
root.title("Stern-Gerlach Simulator")

# First analyzer
axis1_var = tk.StringVar(value="z")
tk.Label(root, text="First analyzer axis:").pack()
tk.OptionMenu(root, axis1_var, "x", "y", "z", "θ").pack()

tk.Label(root, text="Theta value (if first analyzer = θ):").pack()
entry_theta1 = tk.Entry(root)
entry_theta1.insert(0, "0")
entry_theta1.pack()

# Filter choice
filter_var = tk.StringVar(value="up")
tk.Label(root, text="Filter outcome from first analyzer:").pack()
tk.OptionMenu(root, filter_var, "up", "down").pack()

# Second analyzer
axis2_var = tk.StringVar(value="z")
tk.Label(root, text="Second analyzer axis:").pack()
tk.OptionMenu(root, axis2_var, "x", "y", "z", "θ").pack()

tk.Label(root, text="Theta value (if second analyzer = θ):").pack()
entry_theta2 = tk.Entry(root)
entry_theta2.insert(0, "0")
entry_theta2.pack()

# Number of atoms
tk.Label(root, text="Number of atoms:").pack()
entry_atoms = tk.Entry(root)
entry_atoms.insert(0, "10000")
entry_atoms.pack()

# Run button
tk.Button(root, text="Run Sequential Measurement", command=run_two_measurements).pack(pady=5)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
