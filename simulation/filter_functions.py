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

def F_UDD(omega, t, n):
    j = np.arange(1, n + 1)
    t_pulses = t * np.sin(j * np.pi / (2 * (n + 1)))**2
    t_boundaries = np.concatenate([[0], t_pulses, [t]])
    
    omega = np.atleast_1d(omega)
    result = np.zeros(len(omega), dtype=complex)
    
    for k in range(n + 1):
        t_k = t_boundaries[k]
        t_k1 = t_boundaries[k + 1]
        sign = (-1)**k
        safe_omega = np.where(omega == 0, 1, omega)
        result += sign * (np.exp(1j * omega * t_k1) - np.exp(1j * omega * t_k)) / (1j * safe_omega)
    
    F = np.abs(result)**2
    F = np.where(omega == 0, 0, F)
    return F