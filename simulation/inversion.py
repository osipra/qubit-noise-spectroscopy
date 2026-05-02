import sys
sys.path.append('../simulation')
from chi_computation import compute_chi
from filter_functions import F_CPMG
import numpy as np

import numpy as np

def alvarez_suter(t, n_list, omega, S_omega):
    omega_probe = []
    S_reconstructed = []
    
    for n in n_list:
        F_vals = F_CPMG(omega, t, n)
        
        chi = compute_chi(omega, S_omega, F_vals)
        
        omega_n =  n * np.pi / t
        
        F_peak = np.max(F_vals)
        
        S_n = chi * 2 * np.pi / (np.trapz(F_vals, omega))
        
        omega_probe.append(omega_n)
        S_reconstructed.append(S_n)
    
    return np.array(omega_probe), np.array(S_reconstructed)


def tikhonov(t_list, chi_list, omega_recon, lambda_reg): #In-Progress
    d_omega = np.diff(omega_recon, prepend=omega_recon[0])
    
    K = np.zeros((len(t_list), len(omega_recon)))
    for i, t in enumerate(t_list):
        n = max(1, i // 10 + 1)
        K[i, :] = F_CPMG(omega_recon, t, n) * d_omega / (2 * np.pi)
    
    chi_vec = np.array(chi_list)
    S = np.linalg.solve(
        K.T @ K + lambda_reg * np.eye(len(omega_recon)),
        K.T @ chi_vec
    )
    S = np.clip(S, 0, None)
    return omega_recon, S

