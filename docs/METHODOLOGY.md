# Q-Guard: Experimental Methodology

## 1. Overview
Q-Guard is an educational and benchmarking quantum simulation framework designed for the Hackathon Basic Track. It investigates quantum error detection, state preparation, and postselection on noisy intermediate-scale quantum (NISQ) systems.

---

## 2. Quantum State Preparation
The target entangled Bell pair is the maximally entangled state:
$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

State preparation circuit:
```
q0: ──H──■──
         │  
q1: ─────■──
```
In an ideal quantum system, the density matrix $\rho_{\text{ideal}} = |\Phi^+\rangle\langle\Phi^+|$ exhibits perfect correlation:
$$\langle XX \rangle = +1.0, \quad \langle YY \rangle = -1.0, \quad \langle ZZ \rangle = +1.0$$

---

## 3. Pauli Basis Measurements & Rotations
To evaluate the expectation values of tensor product Pauli observables with computational basis ($Z$-basis) measurements, pre-measurement unitary rotations are applied:

1. **$ZZ$ Observable:**
   Direct measurement in the computational basis.
   Eigenvalues: $|00\rangle, |11\rangle \to +1$; $|01\rangle, |10\rangle \to -1$.

2. **$XX$ Observable:**
   $X = H Z H$. Apply Hadamard ($H$) on both data qubits before measurement:
   ```
   q0: ──H──[M]
   q1: ──H──[M]
   ```

3. **$YY$ Observable:**
   $Y = S^\dagger H Z H S$. Apply Phase dagger ($S^\dagger$) followed by Hadamard ($H$) on both data qubits before measurement:
   ```
   q0: ──Sdg──H──[M]
   q1: ──Sdg──H──[M]
   ```

---

## 4. Ancilla-Assisted Parity Check & Postselection
The protected circuit introduces an ancilla qubit ($q_a = q_2$) initialized in $|0\rangle$:
```
q0: ──H──■───■────────[Basis Rot]──[M]
         │   │
q1: ─────■───┼───■────[Basis Rot]──[M]
             │   │
qa: ─────────■───■─────────────────[M]
```
The two CNOT gates compute the parity of the data qubits onto the ancilla:
- Even parity states ($|00\rangle, |11\rangle$): ancilla remains $|0\rangle$.
- Odd parity states ($|01\rangle, |10\rangle$): ancilla is flipped to $|1\rangle$.

### Postselection Rule
- If ancilla $q_a = 0$: The shot is **accepted** (no parity violation detected).
- If ancilla $q_a = 1$: The shot is **rejected / discarded** (parity error detected).

The acceptance rate is defined as:
$$\text{Acceptance Rate} = \frac{N_{\text{accepted}}}{N_{\text{total}}}$$

---

## 5. Fidelity Estimation & Statistical Uncertainty

### Bell State Fidelity
For the $|\Phi^+\rangle$ state, the quantum fidelity $F(\rho) = \langle\Phi^+|\rho|\Phi^+\rangle$ decomposes into Pauli expectation values:
$$F = \frac{1 + \langle XX \rangle - \langle YY \rangle + \langle ZZ \rangle}{4}$$

### Statistical Uncertainty Propagation
For an observable $M \in \{XX, YY, ZZ\}$ evaluated from $N_M$ accepted shots:
$$\langle M \rangle = \frac{N_{\text{even}} - N_{\text{odd}}}{N_M}$$
The variance of a single two-outcome measurement with outcomes $\pm 1$ is $\operatorname{Var}(M) = 1 - \langle M \rangle^2$.
The standard error of the mean is:
$$\sigma_M = \sqrt{\frac{1 - \langle M \rangle^2}{N_M}}$$

Because $XX$, $YY$, and $ZZ$ are measured in independent runs, their statistical fluctuations are uncorrelated. Using Gaussian error propagation:
$$\sigma_F = \frac{1}{4} \sqrt{\sigma_{XX}^2 + \sigma_{YY}^2 + \sigma_{ZZ}^2}$$

### Classical Threshold Decision Rule
The classical threshold for entanglement certification on two qubits is $F > 0.5$. To ensure statistical confidence at the $2\sigma$ level (approx. 95.4% confidence interval), the decision criterion is:
$$\text{Threshold Condition: } F - 2\sigma_F > 0.5$$
The decision and margin $(F - 2\sigma_F - 0.5)$ are reported for every experimental condition.

---

## 6. Physical Noise Modeling
Physical noise channels are simulated via Qiskit Aer:
1. **Single-Qubit Depolarizing Channel:** Applied to all 1Q basis gates ($H, X, Y, Z, S, S^\dagger, T, T^\dagger, \sqrt{X}$).
2. **Two-Qubit Depolarizing Channel:** Applied to all two-qubit $CX$ gates.
3. **Readout Error Channel:** Classical symmetric bit-flip noise applied to measurement operators:
   $$P(1|0) = P(0|1) = p_{\text{readout}}$$
