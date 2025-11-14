from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import random

app = FastAPI()

# Spin states
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


def measure(state, axis: str):
    if axis == "z":
        prob_up = np.abs(np.vdot(Z_plus, state))**2
        return ("up" if random.random() < prob_up else "down")
    elif axis == "x":
        prob_up = np.abs(np.vdot(X_plus, state))**2
        return ("up" if random.random() < prob_up else "down")
    elif axis == "y":
        prob_up = np.abs(np.vdot(Y_plus, state))**2
        return ("up" if random.random() < prob_up else "down")
    else:
        raise ValueError("Invalid axis")


class SimulationRequest(BaseModel):
    axis: str
    trials: int


@app.post("/simulate")
def simulate(req: SimulationRequest):
    up_count = 0
    down_count = 0

    for _ in range(req.trials):
        psi = random_state()
        outcome = measure(psi, req.axis)
        if outcome == "up":
            up_count += 1
        else:
            down_count += 1

    return {"axis": req.axis, "up": up_count, "down": down_count}
