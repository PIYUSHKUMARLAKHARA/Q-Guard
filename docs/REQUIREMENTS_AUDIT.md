# Q-Guard: Hackathon Basic Track Requirements Audit

## 1. Context & Specification Status
- **Hackathon Track:** Basic Track — Quantum Error Detection and Protection Optimizer
- **Challenge Specification Document:** No official organizer PDF or hardware parameter specification was provided in the local workspace repository.
- **Audit Policy:** Per hackathon submission integrity rules, no official requirements or hardware parameters are fabricated. Where official specifications are absent, Q-Guard provides a fully configurable architecture equipped with clearly documented, illustrative placeholder parameters.

---

## 2. Requirements Matrix

| Requirement Item | Description | Status | Verification / Action Required |
| :--- | :--- | :--- | :--- |
| **REQ-01: Bell State Preparation** | Prepare $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$ on data qubits. | **Implemented & Verified** | Verified via statevector and computational basis measurements ($\langle XX\rangle=1, \langle YY\rangle=-1, \langle ZZ\rangle=1$). |
| **REQ-02: Multi-Basis Pauli Measurements** | Measure $XX$, $YY$, and $ZZ$ Pauli observables with appropriate pre-measurement basis rotation gates. | **Implemented & Verified** | $XX$ ($H \otimes H$), $YY$ ($S^\dagger H \otimes S^\dagger H$), $ZZ$ (direct computational basis). |
| **REQ-03: Parity-Check Circuit** | Implement ancilla-based $ZZ$ parity check via CNOT gates to detect bit-flip errors. | **Implemented & Verified** | Data qubits $q_0, q_1$ coupled to ancilla $q_a$. Detects bit flips ($X$) on data qubits. |
| **REQ-04: Postselection Filtering** | Discard shots where ancilla register measures $1$ (odd parity/error detected), retaining $0$. | **Implemented & Verified** | Implemented in post-processing; acceptance rate and discarded shots tracked explicitly. |
| **REQ-05: Simulation Modes** | Support Ideal reference, Noisy baseline, and Noisy + Protection configurations. | **Implemented & Verified** | Executed across all 3 processor profiles using Qiskit Aer. |
| **REQ-06: Processor Profiles** | Configurable physical processor configurations (qubits, coupling graph, noise rates). | **Implemented & Verified** | Configured in `config/processors.json`. Prominently labelled as illustrative defaults. |
| **REQ-07: Error Rate & Noise Modeling** | Depolarizing noise (1Q/2Q) and symmetric readout error models. | **Implemented & Verified** | Built via `qiskit_aer.noise.NoiseModel`. Validated via unit tests and verification scripts. |
| **REQ-08: Circuit Metrics Tracking** | Track depth, 1Q gates, 2Q gates, SWAP counts, and physical qubit footprints. | **Implemented & Verified** | Transpilation with `CouplingMap` preserves and logs physical resource metrics. |
| **REQ-09: Bell State Fidelity Estimation** | Compute quantum state fidelity $F = \frac{1 + \langle XX\rangle - \langle YY\rangle + \langle ZZ\rangle}{4}$. | **Implemented & Verified** | Mathematically verified for $|\Phi^+\rangle$; bounded in $[0, 1]$. |
| **REQ-10: Statistical Uncertainty** | Compute sample standard error $\sigma_M$ for observables and propagate to $\sigma_F$. | **Implemented & Verified** | Standard error of sample mean $\sigma_M = \sqrt{(1 - \langle M\rangle^2)/N}$; error propagation $\sigma_F = \frac{1}{4}\sqrt{\sum \sigma_M^2}$. |
| **REQ-11: Threshold Decision Rule** | Test $F - 2\sigma_F > 0.5$ (statistical confidence of exceeding classical fidelity bound). | **Implemented & Verified** | Evaluated per experiment; reports boolean decision and margin. |
| **REQ-12: Multi-Seed Statistical Validation** | Validate stability across independent simulator seeds to assess variance. | **Implemented & Verified** | 10 independent seeds per configuration executed by `scripts/validate_seeds.py`. |
| **REQ-13: Official Challenge Parameters** | Specific organizer processor parameters, coupling graphs, noise rates, and fixed port qubits. | **Blocked by Missing Official Document** | Awaiting official organizer PDF. Configuration file `config/processors.json` is ready to accept official values instantly. |

---

## 3. Documents & Parameters Needed for Full Official Compliance
To replace the illustrative defaults with the official organizer benchmark parameters:
1. **Organizer Specification Document:** PDF or README specifying exact target chip topology.
2. **Device Calibration Data:**
   - Physical qubit IDs for data ports ($q_0, q_1$) and ancilla ($q_a$).
   - Coupling directed/undirected edge list.
   - Exact single-qubit depolarizing error rate ($p_1$).
   - Exact two-qubit CNOT depolarizing error rate ($p_2$).
   - Measurement readout error probabilities ($p_{0|1}, p_{1|0}$).
3. **Execution Settings:** Target shot count per observable (default: 4096) and official random seeds.
