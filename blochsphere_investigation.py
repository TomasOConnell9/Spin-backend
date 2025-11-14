import numpy as np

# Use your definitions
Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)

def theta_plus(theta_deg, phi_deg):
    θ = np.radians(theta_deg)
    φ = np.radians(phi_deg)
    return np.array([
        np.cos(θ/2),
        np.exp(1j * φ) * np.sin(θ/2)
    ], dtype=complex)

# choose some angles (they can be anything)
theta = 140
phi = 30

# get analyzer spinor
T_plus = theta_plus(theta, phi)

# manually compute the inner product (show algebra)
# <n,+|y,+> = conj(T_plus[0])*Y_plus[0] + conj(T_plus[1])*Y_plus[1]
term1 = np.conjugate(T_plus[0]) * Y_plus[0]
term2 = np.conjugate(T_plus[1]) * Y_plus[1]

print("Term 1 =", term1)
print("Term 2 =", term2)
print("Sum (amplitude) =", term1 + term2)
print("Abs^2 (Pup) =", abs(term1 + term2)**2)
