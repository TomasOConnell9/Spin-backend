from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import random
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Basis states ---
Z_plus = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)
X_plus = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)
Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)

# --- Quantum functions ---
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
    if axis == "x":
        return measure_x(state)
    elif axis == "y":
        return measure_y(state)
    elif axis == "z":
        return measure_z(state)
    else:
        raise ValueError("Invalid axis")

# --- Convert calculator input to Python ---
def convert_expression(expr: str) -> str:
    if not expr:
        return expr
    expr = re.sub(r"√\(([^)]+)\)", r"(\1)**0.5", expr)
    expr = expr.replace("^", "**")
    expr = expr.replace("i", "j")
    return expr

# --- Request model ---
class MeasurementRequest(BaseModel):
    axis1: str
    axis2: str
    filter_choice: str  # up, down, both
    atoms: int
    a: str = None       # optional manual state
    b: str = None

# --- API endpoint ---
@app.post("/two_measurements")
def two_measurements(req: MeasurementRequest):
    first_up = first_down = second_up = second_down = 0

    for _ in range(req.atoms):
        # --- Determine initial state ---
        if req.a and req.b:
            try:
                a_str = convert_expression(req.a)
                b_str = convert_expression(req.b)
                a = complex(eval(a_str))
                b = complex(eval(b_str))
                psi = np.array([a, b], dtype=complex)
                psi /= np.linalg.norm(psi)
            except Exception:
                return {"error": "Invalid input. Use 1, 0.5, 1j, 0.5+0.5j, 1/2**0.5, √5, etc."}
        else:
            psi = random_state()

        # --- First measurement ---
        collapsed_state, outcome1 = measure(psi, req.axis1)
        if outcome1 == "up":
            first_up += 1
        else:
            first_down += 1

        # --- Determine if second measurement is done ---
        if req.filter_choice == "both" or outcome1 == req.filter_choice:
            _, outcome2 = measure(collapsed_state, req.axis2)
            if outcome2 == "up":
                second_up += 1
            else:
                second_down += 1

    return {
        "first_up": first_up,
        "first_down": first_down,
        "second_up": second_up,
        "second_down": second_down
    }
