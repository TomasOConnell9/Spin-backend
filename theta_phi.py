import numpy as np
import random
import tkinter as tk

# --- Spin basis states --- #
Z_plus  = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)
X_plus  = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)
Y_plus  = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)

# --- General θ, φ analyzer states --- #
def theta_plus(theta_deg, phi_deg):
    θ = np.radians(theta_deg)
    φ = np.radians(phi_deg)
    return np.array([
        np.cos(θ/2),
        np.exp(1j * φ) * np.sin(θ/2)
    ], dtype=complex)

def theta_minus(theta_deg, phi_deg):
    θ = np.radians(theta_deg)
    φ = np.radians(phi_deg)
    return np.array([
        -np.exp(-1j * φ) * np.sin(θ/2),
        np.cos(θ/2)
    ], dtype=complex)

# --- Random normalized spin state --- #
def random_state():
    a, b = np.random.randn(2) + 1j*np.random.randn(2)
    vec = np.array([a, b], dtype=complex)
    return vec / np.linalg.norm(vec)

# --- Generic measurement --- #
def measure(state, axis, theta_val=0, phi_val=0):
    if axis == "z":
        up, down = Z_plus, Z_minus
    elif axis == "x":
        up, down = X_plus, X_minus
    elif axis == "y":
        up, down = Y_plus, Y_minus
    elif axis == "θφ":
        up, down = theta_plus(theta_val, phi_val), theta_minus(theta_val, phi_val)
    else:
        raise ValueError("Invalid axis")

    p_up = np.abs(np.vdot(up, state))**2
    if random.random() < p_up:
        return up, "up"
    else:
        return down, "down"

# --- Sequential measurement experiment --- #
def run_two_measurements():
    axis1 = axis1_var.get()
    axis2 = axis2_var.get()
    filt  = filter_var.get()

    # Number of simulated atoms
    try:
        N = int(entry_atoms.get())
    except ValueError:
        result_label.config(text="Enter a valid integer number of atoms.")
        return

    # θ and φ values for second analyzer
    try:
        θ = float(entry_theta.get()) if axis2 == "θφ" else 0
        φ = float(entry_phi.get()) if axis2 == "θφ" else 0
    except ValueError:
        θ, φ = 0, 0

    up2 = down2 = passed = 0

    for _ in range(N):
        ψ = random_state()
        collapsed, out1 = measure(ψ, axis1)
        if out1 == filt:
            passed += 1
            _, out2 = measure(collapsed, axis2, θ, φ)
            if out2 == "up":
                up2 += 1
            else:
                down2 += 1

    if passed == 0:
        result_label.config(text="No atoms passed the first filter!")
        return

    result_label.config(
        text=(
            f"Atoms passed filter: {passed}/{N}\n"
            f"Second analyzer ({axis2.upper()}) results:\n"
            f"Up: {up2}\nDown: {down2}\n"
            f"P(up|filter) = {up2/passed:.3f}, "
            f"P(down|filter) = {down2/passed:.3f}"
        )
    )

# --- Tkinter GUI --- #
root = tk.Tk()
root.title("Two-Analyzer Stern–Gerlach Simulator (θ, φ)")

# Analyzer 1
tk.Label(root, text="First analyzer axis:").pack()
axis1_var = tk.StringVar(value="z")
tk.OptionMenu(root, axis1_var, "x", "y", "z").pack()

# Filter choice
tk.Label(root, text="Filter from first analyzer:").pack()
filter_var = tk.StringVar(value="up")
tk.OptionMenu(root, filter_var, "up", "down").pack()

# Analyzer 2
tk.Label(root, text="Second analyzer axis:").pack()
axis2_var = tk.StringVar(value="z")
tk.OptionMenu(root, axis2_var, "x", "y", "z", "θφ").pack()

# θ, φ input boxes
tk.Label(root, text="If θφ selected, enter θ (degrees):").pack()
entry_theta = tk.Entry(root)
entry_theta.insert(0, "45")
entry_theta.pack()

tk.Label(root, text="Enter φ (degrees):").pack()
entry_phi = tk.Entry(root)
entry_phi.insert(0, "0")
entry_phi.pack()

# Number of atoms
tk.Label(root, text="Number of atoms:").pack()
entry_atoms = tk.Entry(root)
entry_atoms.insert(0, "10000")
entry_atoms.pack()

# Run button
tk.Button(root, text="Run Sequential Measurement", command=run_two_measurements).pack(pady=6)

# Output label
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
