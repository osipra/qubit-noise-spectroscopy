import numpy as np

def compute_chi(omega, S, F):
    integrand = S * F
    return np.trapz(integrand, omega) / (2 * np.pi)