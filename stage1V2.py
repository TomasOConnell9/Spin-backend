from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import random
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://spin-interface.vercel.app", "https://stern-gerlach-demo.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Spin basis states --- #
Z_plus = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)

X_plus = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)

Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)

# --- General θ, φ analyzer states --- #
def theta_plus(theta: float, phi: float = 0):
    θ = np.radians(theta)
    φ = np.radians(phi)
    return np.array([
        np.cos(θ / 2),
        np.exp(1j * φ) * np.sin(θ / 2)
    ], dtype=complex)

def theta_minus(theta: float, phi: float = 0):
    θ = np.radians(theta)
    φ = np.radians(phi)
    return np.array([
        -np.exp(-1j * φ) * np.sin(θ / 2),
        np.cos(θ / 2)
    ], dtype=complex)

# --- Random normalized spin state --- #
def random_state():
    vec = np.random.randn(2) + 1j * np.random.randn(2)
    vec /= np.linalg.norm(vec)
    return vec

# --- Measurement function --- #
def measure(state: np.ndarray, axis: str, theta: float = None, phi: float = 0):
    if axis == "x":
        probs = [abs(np.vdot(X_plus, state))**2, abs(np.vdot(X_minus, state))**2]
        outcome = "up" if random.random() < probs[0] else "down"
        return (X_plus if outcome == "up" else X_minus, outcome)

    elif axis == "y":
        probs = [abs(np.vdot(Y_plus, state))**2, abs(np.vdot(Y_minus, state))**2]
        outcome = "up" if random.random() < probs[0] else "down"
        return (Y_plus if outcome == "up" else Y_minus, outcome)

    elif axis == "z":
        probs = [abs(np.vdot(Z_plus, state))**2, abs(np.vdot(Z_minus, state))**2]
        outcome = "up" if random.random() < probs[0] else "down"
        return (Z_plus if outcome == "up" else Z_minus, outcome)

    elif axis == "θ" or axis == "θφ":
        if theta is None:
            raise ValueError("Theta value must be provided for axis 'θ' or 'θφ'.")
        T_plus = theta_plus(theta, phi)
        T_minus = theta_minus(theta, phi)
        probs = [abs(np.vdot(T_plus, state))**2, abs(np.vdot(T_minus, state))**2]
        outcome = "up" if random.random() < probs[0] else "down"
        return (T_plus if outcome == "up" else T_minus, outcome)

    else:
        raise ValueError("Invalid axis. Choose x, y, z, θ, or θφ.")

# --- Expression converter for a, b inputs --- #
def convert_expression(expr: str) -> str:
    if not expr:
        return expr
    expr = re.sub(r"√\(([^)]+)\)", r"(\1)**0.5", expr)
    expr = expr.replace("^", "**").replace("i", "j")
    return expr

# --- Input models --- #
class AnalyzerInput(BaseModel):
    axis: str
    filter: str = "both"   # up, down, both
    theta: float = None    # optional polar angle
    phi: float = 0         # ✅ new azimuthal angle (default 0°)

class MeasurementRequest(BaseModel):
    analyzers: list[AnalyzerInput]
    atoms: int
    a: str = None
    b: str = None
    forget: bool = False

# --- Main measurement endpoint --- #
@app.post("/measurements")
def run_measurements(req: MeasurementRequest):
    counts = [{"up": 0, "down": 0} for _ in req.analyzers]

    for _ in range(req.atoms):
        # Initialize state
        if req.a and req.b:
            try:
                a = complex(eval(convert_expression(req.a)))
                b = complex(eval(convert_expression(req.b)))
                state = np.array([a, b], dtype=complex)
                state /= np.linalg.norm(state)
            except Exception:
                return {"error": "Invalid a/b values"}
        else:
            state = random_state()

        for i, an in enumerate(req.analyzers):
            state, outcome = measure(state, an.axis, theta=an.theta, phi=an.phi)

            # Apply filtering
            if an.filter != "both" and outcome != an.filter:
                break

            counts[i][outcome] += 1

            # Optional randomization between analyzers
            if req.forget and i < len(req.analyzers) - 1:
                state = random_state()

    return {"results": counts}
