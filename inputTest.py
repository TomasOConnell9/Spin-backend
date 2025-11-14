import numpy as np

def get_manual_state():
    print("Enter the coefficients for your quantum state ψ = a|1> + b|2>")
    
    a_str = input("Enter a (e.g., 1, 0.5, 1j, 0.5+0.5j, 1/root(2)): ")
    b_str = input("Enter b (e.g., 1, 0.5, 1j, 0.5+0.5j, 1j/root(2)): ")
    
    # Replace root(n) with n**0.5
    a_str = a_str.replace("root", "")
    b_str = b_str.replace("root", "")
    
    try:
        # Evaluate **0.5 for roots
        a = complex(eval(a_str.replace("/", "/")))
        b = complex(eval(b_str.replace("/", "/")))
    except Exception:
        print("Invalid input. Use numbers like 1, 0.5, 1j, 0.5+0.5j, 1/2**0.5")
        return None

    vec = np.array([a, b], dtype=complex)
    norm = np.linalg.norm(vec)
    
    if norm == 0:
        print("State cannot be [0, 0].")
        return None
    
    vec /= norm
    return vec

psi = get_manual_state()
if psi is not None:
    print("Normalized state vector:", psi)
