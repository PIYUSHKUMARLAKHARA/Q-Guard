# Q-Guard: Final Experimental Report
**Track:** Hackathon Basic Track  
**Objective:** Quantum Error Detection and Protection Optimizer using Qiskit Aer  

---

## 1. Executive Summary
The Q-Guard experiment systematically evaluates the preparation and verification of the Bell state $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$ across three distinct processor topologies:
1. **2016-Inspired** (5 qubits, linear topology)
2. **Contemporary** (7 qubits, heavy-hex topology)
3. **Hyperbolic-Inspired** (9 qubits, high-connectivity planar graph)

For each processor, three experimental cases were measured across $XX$, $YY$, and $ZZ$ Pauli bases:
- **Ideal:** State preparation with zero noise.
- **Noisy:** Baseline simulation under physical depolarizing and readout noise.
- **Noisy + Protection:** Ancilla-assisted $ZZ$ parity check with postselection filtering.

---

## 2. Experimental Results Table

| Processor | Experiment | Estimated Fidelity $F$ | Statistical Uncertainty $\sigma_F$ | $F - 2\sigma_F$ | Threshold $(> 0.5)$ | Acceptance Rate | Depth | 2Q Gates |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2016-Inspired | Ideal | 1.00000 | 0.00000 | 1.00000 | PASS | 100.0% | 4.0 | 1.0 |
| 2016-Inspired | Noisy | 0.92102 | 0.00302 | 0.91498 | PASS | 100.0% | 4.0 | 1.0 |
| 2016-Inspired | Noisy + Protection | 0.88507 | 0.00377 | 0.87753 | PASS | 91.1% | 9.0 | 6.0 |
| Contemporary | Ideal | 1.00000 | 0.00000 | 1.00000 | PASS | 100.0% | 4.0 | 1.0 |
| Contemporary | Noisy | 0.96277 | 0.00211 | 0.95856 | PASS | 100.0% | 4.0 | 1.0 |
| Contemporary | Noisy + Protection | 0.94491 | 0.00260 | 0.93970 | PASS | 95.5% | 9.0 | 6.0 |
| Hyperbolic-Inspired | Ideal | 1.00000 | 0.00000 | 1.00000 | PASS | 100.0% | 4.0 | 1.0 |
| Hyperbolic-Inspired | Noisy | 0.94409 | 0.00256 | 0.93897 | PASS | 100.0% | 4.0 | 1.0 |
| Hyperbolic-Inspired | Noisy + Protection | 0.92835 | 0.00297 | 0.92241 | PASS | 94.2% | 9.0 | 6.0 |

---

## 3. Key Scientific Findings & Analysis

1. **Entanglement Witness / Classical Threshold:**
   All processors and configurations successfully exceeded the classical limit ($F - 2\sigma_F > 0.5$) with high statistical confidence, demonstrating genuine two-qubit entanglement.

2. **Error Protection Trade-Off:**
   In all three simulated topologies, **protected fidelity is lower than the noisy baseline**:
   - The ancilla parity check adds 2 syndrome CNOT gates, plus additional routing gates (totaling 6 two-qubit CX gates vs 1 in baseline), increasing circuit depth from 4 to 9.
   - Under realistic physical noise rates ($p_2 \sim 10^{-2}$), the gate noise introduced by the extra CNOTs outweighs the error-filtering capability of the single-ancilla ZZ parity check.
   - The parity check detects bit-flip ($X$) and bit-phase ($Y$) errors, but is completely blind to phase-flip ($Z$) errors because $Z$ commutes with $Z \otimes Z$.

3. **Topology Impact:**
   - The **Contemporary** processor with lower 2-qubit noise ($p_2 = 0.012$) achieved the highest fidelity ($F \approx 0.963$ baseline, $0.945$ protected).
   - Higher connectivity reduces routing overhead, but gate fidelity remains the primary bottleneck.

---

## 4. Submission Artifacts
- Raw results: `outputs/experiment_results.csv`
- Protection analysis: `outputs/protection_analysis.csv`
- Multi-seed report: `outputs/final_multi_seed_report.csv`
- Visualizations:
  - `outputs/fidelity_comparison.png`
  - `outputs/acceptance_rate.png`
  - `outputs/circuit_overhead.png`
  - `outputs/processor_comparison.png`
