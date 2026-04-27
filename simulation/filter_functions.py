import numpy as np

def F_Ramsey(omega, t):
    return np.where(omega == 0, t ** 2, (4 * (np.sin(omega * t / 2) ** 2)) / (omega ** 2))

def F_Hahn(omega, t):
    return np.where(omega == 0, 0 , (16 * (np.sin(omega * t / 4) ** 4) / omega ** 2))