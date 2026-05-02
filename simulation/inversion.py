import sys
sys.path.append('../simulation')
from chi_computation import compute_chi
from noise_models import pink_noise, white_noise, lorentzian_noise, total_noise
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

def bayesian_spectroscopy(omega, S_true, n_experiments=50, sigma_rel=0.1,
                          A_bounds=(4,9), alpha_bounds=(0.5,1.5), S0_bounds=(0,4)):
    A_grid     = np.logspace(*A_bounds,     20)
    alpha_grid = np.linspace(*alpha_bounds, 20)
    S0_grid    = np.logspace(*S0_bounds,    20)

    # Precompute all S models — shape (20, 20, 20, len(omega))
    A  = A_grid[:, None, None, None]
    al = alpha_grid[None, :, None, None]
    S0 = S0_grid[None, None, :, None]
    om = omega[None, None, None, :]

    S_models = np.where(om == 0, 0, A / om**al) + S0

    # --- FIX 1: work in log-space from the start ---
    log_post = np.zeros((20, 20, 20))          # uniform log-prior

    t_candidates = np.logspace(-6, -3, 20)
    n_candidates = np.arange(1, 20)

    for exp in range(n_experiments):
        t = t_candidates[exp % len(t_candidates)]
        n = int(n_candidates[exp % len(n_candidates)])

        F_vals   = F_CPMG(omega, t, n)
        chi_meas = compute_chi(omega, S_true, F_vals)

        # --- FIX 2: / np.pi, not / (2*np.pi) ---
        integrand = S_models * F_vals[None, None, None, :]
        chi_pred  = np.trapz(integrand, omega, axis=-1) / np.pi

        # --- FIX 3: adaptive sigma scales with the measurement ---
        sigma = max(sigma_rel * abs(chi_meas), 1e-6)

        log_like  = -(chi_meas - chi_pred)**2 / (2 * sigma**2)

        # Additive update in log-space, re-centre to prevent overflow
        log_post += log_like
        log_post -= log_post.max()             # shift so max=0 before each step

    idx = np.unravel_index(log_post.argmax(), log_post.shape)
    posterior = np.exp(log_post)
    posterior /= posterior.sum()

    return A_grid[idx[0]], alpha_grid[idx[1]], S0_grid[idx[2]], posterior
