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

# --- Helper functions ---
def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec

def measure_z(state):
    prob_up = np.abs(np.vdot(Z_plus, state))**2
    return (Z_plus, "up") if random.random() < prob_up else (Z_minus, "down")

def measure_x(state):
    prob_up = np.abs(np.vdot(X_plus, state))**2
    return (X_plus, "up") if random.random() < prob_up else (X_minus, "down")

def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    return (Y_plus, "up") if random.random() < prob_up else (Y_minus, "down")

def measure(state, axis):
    if axis == "z": return measure_z(state)
    if axis == "x": return measure_x(state)
    if axis == "y": return measure_y(state)
    raise ValueError("Invalid axis. Choose x, y, or z.")

# --- Main simulation ---
def run_three_measurements():
    axis1 = axis1_var.get()
    axis2 = axis2_var.get()
    axis3 = axis3_var.get()
    filter1 = filter1_var.get()
    filter2 = filter2_var.get()
    forget = forget_var.get()

    try:
        N = int(entry_atoms.get())
    except ValueError:
        result_label.config(text="Please enter a valid number of atoms.")
        return

    second_up = second_down = 0
    third_up = third_down = 0

    for _ in range(N):
        psi = random_state()
        collapsed_state1, outcome1 = measure(psi, axis1)

        # First filter
        if filter1 == "both" or outcome1 == filter1:
            collapsed_state2, outcome2 = measure(collapsed_state1, axis2)

            # Second filter
            if filter2 == "both" or outcome2 == filter2:
                if outcome2 == "up":
                    second_up += 1
                else:
                    second_down += 1

                # Third analyzer
                if forget:
                    collapsed_state2 = random_state()
                _, outcome3 = measure(collapsed_state2, axis3)
                if outcome3 == "up":
                    third_up += 1
                else:
                    third_down += 1

    forget_text = "(forgetting enabled)" if forget else ""
    result_label.config(
        text=f"Second measurement ({axis2.upper()}):\n"
             f"  Up:   {second_up}\n"
             f"  Down: {second_down}\n\n"
             f"Third measurement ({axis3.upper()}) {forget_text}:\n"
             f"  Up:   {third_up}\n"
             f"  Down: {third_down}"
    )

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Three-Analyzer Stern–Gerlach Simulator")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

# Analyzer 1
tk.Label(frame_top, text="First analyzer axis:").grid(row=0, column=0, padx=5, pady=2)
axis1_var = tk.StringVar(value="z")
tk.OptionMenu(frame_top, axis1_var, "x", "y", "z").grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_top, text="Filter outcome (1st):").grid(row=1, column=0, padx=5, pady=2)
filter1_var = tk.StringVar(value="up")
tk.OptionMenu(frame_top, filter1_var, "up", "down", "both").grid(row=1, column=1, padx=5, pady=2)

# Analyzer 2
tk.Label(frame_top, text="Second analyzer axis:").grid(row=0, column=2, padx=5, pady=2)
axis2_var = tk.StringVar(value="y")
tk.OptionMenu(frame_top, axis2_var, "x", "y", "z").grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_top, text="Filter outcome (2nd):").grid(row=1, column=2, padx=5, pady=2)
filter2_var = tk.StringVar(value="up")
tk.OptionMenu(frame_top, filter2_var, "up", "down", "both").grid(row=1, column=3, padx=5, pady=2)

# Analyzer 3
tk.Label(frame_top, text="Third analyzer axis:").grid(row=2, column=0, padx=5, pady=2)
axis3_var = tk.StringVar(value="z")
tk.OptionMenu(frame_top, axis3_var, "x", "y", "z").grid(row=2, column=1, padx=5, pady=2)

# Forget checkbox
forget_var = tk.BooleanVar(value=False)
tk.Checkbutton(frame_top, text="Forget collapsed state before 3rd analyzer", variable=forget_var).grid(row=2, column=2, columnspan=2, pady=5)

# Number of atoms
tk.Label(root, text="Number of atoms:").pack()
entry_atoms = tk.Entry(root)
entry_atoms.insert(0, "10000")
entry_atoms.pack()

# Run button
tk.Button(root, text="Run Three Measurements", command=run_three_measurements).pack(pady=8)

# Results
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
