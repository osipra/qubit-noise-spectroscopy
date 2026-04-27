# Qubit Noise Spectroscopy

A complete, reusable pipeline for characterizing the noise power spectral density $S(\omega)$ of a superconducting qubit — from first principles derivation to IBM hardware validation.

Built as part of ECE 676 / QIC 750 / PHYS 768 at the University of Waterloo.

---

## Motivation

Decoherence is the central obstacle in quantum computing. A qubit in a superposition state accumulates random phase from environmental noise, causing the Bloch vector to dephase and lose coherence. Understanding *which frequencies* of noise are responsible — and how strongly — is prerequisite to suppressing them.

This project uses the qubit itself as a precision noise sensor. By applying carefully designed pulse sequences (dynamical decoupling) and measuring the resulting coherence decay, we reconstruct the full noise power spectral density $S(\omega)$ of the qubit's environment. The key relation is:

$$\chi(t) = \int_0^\infty \frac{d\omega}{2\pi} S(\omega) F(\omega, t)$$

where $\chi(t)$ is the coherence decay exponent measured in experiment, and $F(\omega, t)$ is the **filter function** — the frequency-selective sensitivity of the pulse sequence. Different sequences probe different spectral windows, enabling full reconstruction of $S(\omega)$.

---

## Project Scope

### Pulse Sequences
| Sequence | Filter peak | Role |
|---|---|---|
| Ramsey | $\omega = 0$ | Low-frequency / $1/f$ noise |
| Hahn echo | $\omega = 2\pi/t$ | Bandpass, baseline DD |
| CPMG-$n$ | $\omega = n\pi/t$ | Tunable bandpass |
| XY-8 | $\omega = 8\pi/t$ | Phase-cycled, robust to pulse errors |
| UDD-$n$ | Nonuniform spacing | Optimal suppression for smooth $S(\omega)$ |

### Noise Models
- $1/f^\alpha$ noise (charge noise, flux noise)
- White noise floor
- Lorentzian peaks from two-level system (TLS) defects

### Inversion Methods
Three independent methods for reconstructing $S(\omega)$ from measured $\chi(t)$:

1. **Álvarez-Suter discrete derivative** — direct inversion using CPMG filter orthogonality
2. **Tikhonov regularization** — least-squares inversion with regularization to handle ill-conditioning
3. **Bayesian adaptive spectroscopy** — dynamically selects the next pulse sequence to maximally reduce posterior uncertainty in $S(\omega)$; state-of-the-art approach used in cutting-edge labs

### Cross-Validation
- **Randomized benchmarking spectroscopy (NSRB)** — independent $S(\omega)$ estimate from randomized sequences, robust to systematic pulse errors; cross-validated against DD-based reconstruction

### Hardware
- All sequences implemented and validated on **ibm_marrakesh** via Qiskit
- $T_1$, $T_2^*$, $T_2$ characterized as a function of time of day to capture temporal drift of $S(\omega)$
- $S(\omega)$ reconstructed and compared across multiple qubits on ibm_marrakesh
- Full uncertainty quantification: shot noise, gate errors, SPAM errors

### Out of Scope
- $T_1$ noise spectroscopy (transverse noise)
- Non-Gaussian noise beyond Lorentzian TLS model
- Optimal control or active noise suppression

---

## Repository Structure

```
qubit-noise-spectroscopy/
├── README.md
├── theory/
│   ├── 01_qubit_decoherence.tex                    # T1, T2, Lindblad, Bloch sphere
│   ├── 02_filter_function_formalism.tex             # Core derivation from first principles
│   ├── 03_filter_functions_sequences.tex            # Ramsey, Hahn, CPMG, XY-8, UDD
│   ├── 04_noise_models.tex                          # 1/f, white noise, TLS Lorentzians
│   ├── 05_inversion_problem.tex                     # χ(t) → S(ω), ill-conditioning
│   ├── 06_alvarez_suter.tex                         # Discrete derivative method
│   ├── 07_tikhonov_regularization.tex               # Regularized least-squares inversion
│   ├── 08_bayesian_adaptive_spectroscopy.tex        # Posterior updates, experiment selection
│   ├── 09_randomized_benchmarking.tex               # NSRB, connection to DD methods
│   ├── 10_uncertainty_quantification.tex            # Shot noise, SPAM, error propagation
│   └── references.bib                               # Shared bibliography
├── simulation/
│   ├── filter_functions.py                          # F(ω,t) for all sequences
│   ├── noise_models.py                              # S(ω) definitions
│   ├── chi_computation.py                           # Numerical integration of χ(t)
│   └── inversion.py                                 # S(ω) reconstruction methods
├── hardware/
│   ├── circuits.py                                  # Qiskit pulse sequences
│   └── analysis.py                                  # Extracting χ(t) from hardware data
├── visualization/
│   └── bloch_visualization.py                       # Bloch sphere decoherence animation
└── notebooks/
    ├── 01_filter_functions.ipynb                    # F(ω,t) derivation and visualization
    ├── 02_noise_models.ipynb                        # S(ω) models and χ(t) simulation
    ├── 03_inversion.ipynb                           # S(ω) reconstruction and comparison
    └── 04_hardware_validation.ipynb                 # IBM hardware results
```

---

## Theory Summary

### Filter Function Derivation

For a qubit subject to stochastic frequency noise $\delta\omega(t)$, the coherence decay exponent is:

$$\chi(t) = \frac{1}{2}\langle\varphi^2(t)\rangle, \qquad \varphi(t) = \int_0^t f(t')\,\delta\omega(t')\,dt'$$

where $f(t') \in \{+1, -1\}$ is the modulation function encoding the pulse sequence. Applying the Wiener-Khinchin theorem:

$$\chi(t) = \int_0^\infty \frac{d\omega}{2\pi}\,S(\omega)\,F(\omega,t), \qquad F(\omega,t) = \left|\int_0^t f(t')\,e^{i\omega t'}\,dt'\right|^2$$

### Ramsey Filter Function

$$F_\text{Ramsey}(\omega, t) = \frac{4\sin^2(\omega t/2)}{\omega^2}$$

Peaks at $\omega = 0$ — maximally sensitive to low-frequency/$1/f$ noise.

### Hahn Echo Filter Function

$$F_\text{Hahn}(\omega, t) = \frac{16\sin^4(\omega t/4)}{\omega^2}$$

Zero at $\omega = 0$, peaks at $\omega = 2\pi/t$ — refocuses static noise, acts as bandpass filter.

For full derivations see `theory/02_filter_function_formalism.tex` and `theory/03_filter_functions_sequences.tex`.

---

## Key References

1. L. Cywiński, R. M. Lutchyn, C. P. Nave, S. Das Sarma, *How to enhance dephasing time in superconducting qubits*, PRB **77**, 174509 (2008). [arXiv:0807.4926](https://arxiv.org/abs/0807.4926)

2. G. A. Álvarez and D. Suter, *Measuring the Spectrum of Colored Noise by Dynamical Decoupling*, PRL **107**, 230501 (2011).

3. J. Bylander et al., *Noise spectroscopy through dynamical decoupling with a superconducting flux qubit*, Nature Physics **7**, 565 (2011).

4. C. Granade et al., *Robust online Hamiltonian learning*, NJP **14**, 103013 (2012).

5. T. J. Proctor et al., *Detecting and tracking drift in quantum information processors*, PRL **124**, 010501 (2020).

6. A. A. Clerk et al., *Introduction to quantum noise, measurement, and amplification*, Rev. Mod. Phys. **82**, 1155 (2010).

---

## Requirements

```
qutip
qiskit
qiskit-ibm-runtime
numpy
scipy
matplotlib
```

---

## Status

- [x] Theory derivation (Ramsey, Hahn echo filter functions)
- [x] Bloch sphere decoherence visualization
- [x] Filter functions (CPMG, XY-8, UDD)
- [ ] Noise models
- [ ] Chi(t) numerical computation
- [ ] Inversion methods
- [ ] Bayesian adaptive spectroscopy
- [ ] RB-based spectroscopy
- [ ] IBM hardware validation

---

*University of Waterloo — Institute for Quantum Computing*
