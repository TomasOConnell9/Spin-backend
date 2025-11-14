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
    return (Z_plus, "up") if random.random() < prob_up else (Z_minus, "down")

def measure_x(state):
    prob_up = np.abs(np.vdot(X_plus, state))**2
    return (X_plus, "up") if random.random() < prob_up else (X_minus, "down")

def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    return (Y_plus, "up") if random.random() < prob_up else (Y_minus, "down")

def measure(state, axis):
    if axis == "x": return measure_x(state)
    if axis == "y": return measure_y(state)
    if axis == "z": return measure_z(state)
    raise ValueError("Invalid axis")

# --- Convert input expression ---
def convert_expression(expr: str) -> str:
    if not expr:
        return expr
    expr = re.sub(r"√\(([^)]+)\)", r"(\1)**0.5", expr)
    expr = expr.replace("^", "**")
    expr = expr.replace("i", "j")
    return expr

# --- Request model ---
class ThreeMeasurementRequest(BaseModel):
    axis1: str
    axis2: str
    axis3: str
    filter1: str  # up, down, both
    filter2: str  # up, down, both
    forget: bool = False
    atoms: int
    a: str = None
    b: str = None

# --- API endpoint ---
@app.post("/three_measurements")
def three_measurements(req: ThreeMeasurementRequest):
    second_up = second_down = 0
    third_up = third_down = 0

    for _ in range(req.atoms):
        # --- Initial state ---
        if req.a and req.b:
            try:
                a_str = convert_expression(req.a)
                b_str = convert_expression(req.b)
                a = complex(eval(a_str))
                b = complex(eval(b_str))
                psi = np.array([a, b], dtype=complex)
                psi /= np.linalg.norm(psi)
            except Exception:
                return {"error": "Invalid input for a/b"}
        else:
            psi = random_state()

        # --- First measurement ---
        collapsed1, outcome1 = measure(psi, req.axis1)

        if req.filter1 == "both" or outcome1 == req.filter1:
            collapsed2, outcome2 = measure(collapsed1, req.axis2)

            if req.filter2 == "both" or outcome2 == req.filter2:
                # Count second measurement
                if outcome2 == "up":
                    second_up += 1
                else:
                    second_down += 1

                # Third measurement (forget if needed)
                if req.forget:
                    collapsed2 = random_state()
                _, outcome3 = measure(collapsed2, req.axis3)
                if outcome3 == "up":
                    third_up += 1
                else:
                    third_down += 1

    return {
        "second_up": second_up,
        "second_down": second_down,
        "third_up": third_up,
        "third_down": third_down
    }
