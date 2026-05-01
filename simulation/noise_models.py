import numpy as np

def pink_noise(A, f, alpha):
    return np.where(f == 0, 0, A / f**alpha)

def white_noise(f, A):
    return np.full_like(f, A)

def lorentzian_noise(f, A, f0, gamma):
    return A * gamma ** 2 / ((f - f0) ** 2 + gamma ** 2)

def total_noise(f, A_pink, alpha, A_white, A_lorentzian, f0, gamma):
    pink = pink_noise(A_pink, f, alpha)
    white = white_noise(f, A_white)
    lorentzian = lorentzian_noise(f, A_lorentzian, f0, gamma)
    return pink + white + lorentzian