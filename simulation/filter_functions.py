import numpy as np

def F_Ramsey(omega, t):
    return np.where(omega == 0, t ** 2, (4 * (np.sin(omega * t / 2) ** 2)) / (omega ** 2))

def F_Hahn(omega, t):
    return np.where(omega == 0, 0 , (16 * (np.sin(omega * t / 4) ** 4) / omega ** 2))

def F_CPMG(omega, t, n):
    denom = np.sin(omega * t / (2 * n))
    safe_omega = np.where(omega == 0, 1, omega)
    safe_denom = np.where(denom == 0, 1, denom)
    result = (16 * np.sin(omega * t / (4 * n))**4 / safe_omega**2 
              * np.sin(omega * t / 2)**2 / safe_denom**2)
    result = np.where((omega == 0) | (denom == 0), 0, result)
    return result

def F_XY8(omega, t):
    return F_CPMG(omega, t, 8)