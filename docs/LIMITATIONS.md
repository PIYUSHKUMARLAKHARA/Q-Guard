# Q-Guard: Scientific & Engineering Limitations

## 1. Ancilla Postselection vs. Full Quantum Error Correction (QEC)
- **Error Detection vs. Correction:** The parity-check circuit implemented in Q-Guard is an **error-detecting postselection scheme**, not an active quantum error-correcting code (QECC). Detected errors result in discarded shots rather than active syndrome recovery.
- **Single Observable Parity Check:** The circuit measures only the $Z \otimes Z$ parity stabilizer. Consequently:
  - **Bit-flip errors ($X_0, X_1$):** Detected because $X$ anti-commutes with $Z$, toggling the ancilla to $|1\rangle$.
  - **Bit-and-phase errors ($Y_0, Y_1$):** Detected via the bit-flip component.
  - **Phase-flip errors ($Z_0, Z_1$):** **Undetected**. Phase flips commute with $Z \otimes Z$, leaving the ancilla in state $|0\rangle$ while distorting the relative phase of $|\Phi^+\rangle$ into $|\Phi^-\rangle$.
- **No Fault Tolerance:** The ancilla syndrome extraction does not employ fault-tolerant gadgetry (such as Shor or Steane ancilla verification). A single physical fault during syndrome extraction can propagate into an uncorrectable data error.

---

## 2. NISQ Gate Noise Overhead Trade-Off
In current NISQ devices, two-qubit CNOT gates have substantially higher error rates ($10^{-2}$ to $10^{-3}$) than single-qubit gates ($10^{-3}$ to $10^{-4}$).
- **Unprotected Circuit:** 1 CNOT gate for state preparation.
- **Protected Circuit:** 1 CNOT for state preparation + 2 CNOTs for ancilla parity extraction + 3 SWAP/routing CNOT equivalents depending on hardware connectivity (total: ~6 CNOT operations and 9 depth).
- **Physical Result:** The physical noise introduced by the extra CNOT gates and increased circuit depth exceeds the error-rejection benefit of the postselection filter. Thus, for all simulated profiles, **net protected fidelity is lower than unmitigated noisy fidelity**.
- **Scientific Integrity Principle:** We report this honestly and clearly; postselection without fault tolerance in high-error regimes degrades overall state fidelity.

---

## 3. Simulator Assumptions vs. Real Quantum Hardware
- **Illustrative Processor Profiles:** The device parameters in `config/processors.json` (such as `2016-Inspired`, `Contemporary`, and `Hyperbolic-Inspired`) are illustrative models designed to benchmark topologies and error rates. They do not represent calibrated IBM Quantum, Google Quantum AI, or Rigetti physical hardware runs.
- **Noise Model Simplifications:** Noise is modeled with uniform depolarizing channels and symmetric readout errors. Real hardware exhibits asymmetric $T_1/T_2$ relaxation/dephasing, crosstalk, spectator qubit leakage, and coherent gate over-rotations.
- **Statistical Multi-Seed Variation:** Multi-seed evaluation tests the numerical variance of the pseudorandom simulator runs; it does not replace multi-day physical device drift calibration.
