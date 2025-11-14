from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import random

app = FastAPI()

# Number of atoms
N = 10000

# Pauli states
Z_plus = np.array([1, 0])
Z_minus = np.array([0, 1])
Y_plus = (1/np.sqrt(2)) * np.array([1, 1j])
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j])
X_plus = (1/np.sqrt(2)) * np.array([1, 1])
X_minus = (1/np.sqrt(2)) * np.array([1, -1])

# Pydantic model for request
class SimulationRequest(BaseModel):
    axis: str
    trials: int = N

# Measurement functions
def measure_z_Pauli(state):
    p_up = np.abs(np.vdot(Z_plus, state))**2
    if random.random() < p_up:
        return Z_plus, "up"
    else:
        return Z_minus, "down"

def measure_y_Pauli(state):
    p_up = np.abs(np.vdot(Y_plus, state))**2
    if random.random() < p_up:
        return Y_plus, "up"
    else:
        return Y_minus, "down"

def measure_x_Pauli(state):
    p_up = np.abs(np.vdot(X_plus, state))**2
    if random.random() < p_up:
        return X_plus, "up"
    else:
        return X_minus, "down"

# API endpoint
@app.post("/simulate")
def simulate(req: SimulationRequest):
    trials = req.trials
    axis = req.axis.lower()
    
    if axis == "z":
        atoms = [random.choice([Z_plus, Z_minus]) for _ in range(trials)]
        results = [measure_z_Pauli(p)[1] for p in atoms]
    elif axis == "y":
        atoms = [random.choice([Y_plus, Y_minus]) for _ in range(trials)]
        results = [measure_y_Pauli(p)[1] for p in atoms]
    elif axis == "x":
        atoms = [random.choice([X_plus, X_minus]) for _ in range(trials)]
        results = [measure_x_Pauli(p)[1] for p in atoms]
    else:
        return {"error": "Invalid axis"}

    return {
        "up": results.count("up"),
        "down": results.count("down")
    }
