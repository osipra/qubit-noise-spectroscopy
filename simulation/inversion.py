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