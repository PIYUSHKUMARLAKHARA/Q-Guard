# Q-Guard: Submission Notes & Compliance Summary

## 1. Project Overview & Track
- **Project Name:** Q-Guard — Quantum Error Detection and Protection Optimizer
- **Hackathon Track:** Basic Track
- **Software Framework:** Qiskit 2.5.2 & Qiskit Aer 0.17.2 on Python 3.12.3

---

## 2. Implementation & Verification Status
- **Test Suite:** **55 automated unit tests executed and passed (0 failures, 0 errors)** across:
  - Circuit preparation & basis rotations (`tests/test_circuits.py`)
  - Noise modeling & error channels (`tests/test_noise.py`)
  - Metrics, uncertainty propagation & threshold tests (`tests/test_metrics.py`)
  - Graph topology & processor validation (`tests/test_validation.py`)
  - Transpilation & execution pipeline (`tests/test_experiments.py`)
  - Reporting & visualization generation (`tests/test_reporting.py`)
- **Experimental Pipeline Executed:**
  - Evaluated 3 distinct processor topologies (`2016-Inspired`, `Contemporary`, `Hyperbolic-Inspired`).
  - Evaluated 3 experimental modes (`Ideal`, `Noisy Baseline`, `Noisy + Protection`).
  - Evaluated 3 Pauli observables ($XX, YY, ZZ$) with 4,096 shots each.
- **Statistical Validation:**
  - Multi-seed validation script (`scripts/validate_seeds.py`) executed 10 independent random seeds per condition (60 simulator runs total).
  - Calculated sample mean, standard deviation, and standard error of fidelity and acceptance rates.
- **Controlled Error-Injection Verification:**
  - Verified with `scripts/verify_protection.py`: 100% rejection on injected $X$ bit-flip errors, 100% acceptance on ideal states, 100% acceptance on phase-flip $Z$ errors.

---

## 3. Key Experimental Evidence
1. **Entanglement Witness Decision ($F - 2\sigma_F > 0.5$):**
   - All processors across all conditions strictly satisfied the classical entanglement threshold with >95% confidence (margin $> 0.37$).
2. **Error Protection Trade-Off:**
   - In all three simulated processors, **protected fidelity is lower than the unmitigated noisy baseline**:
     - `2016-Inspired`: Noisy $F = 0.92102 \pm 0.0045$, Protected $F = 0.88507 \pm 0.0056$ ($\Delta F = -0.03595$).
     - `Contemporary`: Noisy $F = 0.96277 \pm 0.0033$, Protected $F = 0.94491 \pm 0.0040$ ($\Delta F = -0.01786$).
     - `Hyperbolic-Inspired`: Noisy $F = 0.94409 \pm 0.0040$, Protected $F = 0.92835 \pm 0.0047$ ($\Delta F = -0.01574$).
   - **Reason:** The ancilla ZZ parity check introduces 2 syndrome CNOT gates and up to 3 routing CNOTs (+5 depth, +5 two-qubit gates). In NISQ systems where two-qubit gate error rates are $\sim 1\% - 2.5\%$, the physical decoherence and gate infidelities introduced by the extraction circuit outweigh the error-filtering capacity of the postselection step.
3. **Acceptance Rates:**
   - 2016-Inspired: $91.1\%$
   - Contemporary: $95.5\%$
   - Hyperbolic-Inspired: $94.2\%$

---

## 4. Important Limitations & Disclaimers
1. **Illustrative Processor Profiles:**
   - The device profiles in `config/processors.json` are illustrative models designed to benchmark topological properties and error scalings. They do not represent official organizer PDF values or real physical quantum hardware calibrations.
2. **Simulator vs. Real Hardware:**
   - All results were gathered via Qiskit Aer simulations. No claims of physical quantum hardware benchmarking are made.
3. **Parity Check Scope:**
   - The parity check detects $X$ and $Y$ errors, but does not detect $Z$ phase errors. It is a postselection filter, not a fault-tolerant quantum error-correcting code (QECC).
4. **No Artificial Claims of Improvement:**
   - The evidence clearly demonstrates a net fidelity drop under physical noise; we report this negative result honestly with full mathematical and architectural explanations.

---

## 5. Outstanding Requirements for Final Official Compliance
If the hackathon committee provides official processor specifications:
1. Update `config/processors.json` with official qubit count, coupling edges, and error rates.
2. Run `python main.py` and `python scripts/make_submission_zip.py`.
