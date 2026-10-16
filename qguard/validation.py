"""
Q-Guard: Configuration and Topology Validation Module.

Validates processor configurations, coupling maps, port qubits,
and noise parameters against physical constraints.
"""

from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


def validate_topology(qubits: int, edges: List[List[int]]) -> Dict[str, Any]:
    """
    Validate coupling graph connectivity, self-loops, degree distribution,
    and connected components.
    """
    if qubits < 2:
        raise ValueError(f"Processor requires at least 2 qubits, got {qubits}")

    adjacency: Dict[int, Set[int]] = {q: set() for q in range(qubits)}

    for edge in edges:
        if len(edge) != 2:
            raise ValueError(f"Invalid edge specification (must be 2 vertices): {edge}")

        u, v = int(edge[0]), int(edge[1])

        if u == v:
            raise ValueError(f"Self-loops are not allowed in physical coupling: ({u}, {v})")

        if not (0 <= u < qubits and 0 <= v < qubits):
            raise ValueError(
                f"Edge ({u}, {v}) references physical qubits outside range [0, {qubits - 1}]"
            )

        adjacency[u].add(v)
        adjacency[v].add(u)

    degrees = [len(neighbors) for neighbors in adjacency.values()]

    # Connected components using BFS
    visited: Set[int] = set()
    components = 0

    for start in range(qubits):
        if start in visited:
            continue
        components += 1
        queue = deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    is_connected = (components == 1)

    return {
        "qubits": qubits,
        "edges_count": len(edges),
        "average_degree": sum(degrees) / qubits if qubits else 0.0,
        "maximum_degree": max(degrees, default=0),
        "connected_components": components,
        "is_connected": is_connected,
    }


def validate_processor_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the overall processor JSON configuration dictionary.
    """
    if "processors" not in config or not config["processors"]:
        raise ValueError("Configuration missing non-empty 'processors' list.")

    shots = int(config.get("shots", 4096))
    if shots <= 0:
        raise ValueError(f"Shots must be positive integer, got {shots}")

    seed = int(config.get("seed", 42))

    for processor in config["processors"]:
        name = processor.get("name", "Unnamed")
        qubits = int(processor.get("qubits", 0))
        edges = processor.get("edges", [])

        # Validate topology
        validate_topology(qubits, edges)

        # Validate port qubits if specified
        port_qubits = processor.get("port_qubits", [0, 1])
        if len(port_qubits) != 2:
            raise ValueError(f"{name}: 'port_qubits' must specify exactly 2 data qubits.")
        if port_qubits[0] == port_qubits[1]:
            raise ValueError(f"{name}: Port qubits cannot be identical: {port_qubits}")
        for q in port_qubits:
            if not (0 <= q < qubits):
                raise ValueError(f"{name}: Port qubit {q} outside range [0, {qubits - 1}]")

        # Validate ancilla qubit if specified
        ancilla_qubit = processor.get("ancilla_qubit", 2 if qubits > 2 else None)
        if ancilla_qubit is not None:
            if not (0 <= ancilla_qubit < qubits):
                raise ValueError(f"{name}: Ancilla qubit {ancilla_qubit} outside range [0, {qubits - 1}]")
            if ancilla_qubit in port_qubits:
                raise ValueError(f"{name}: Ancilla qubit cannot overlap with port qubits: {ancilla_qubit}")

        # Validate noise parameters
        for param in ("single_qubit_depolarizing", "two_qubit_depolarizing", "readout_error"):
            if param in processor:
                rate = float(processor[param])
                if not 0.0 <= rate <= 1.0:
                    raise ValueError(f"{name}: Noise parameter '{param}' must be in [0, 1], got {rate}")

    return config


def calculate_shortest_distance(processor: Dict[str, Any], start: int = 0, target: int = 1) -> int:
    """Calculate the shortest graph routing distance between physical qubits."""
    qubit_count = int(processor["qubits"])
    if not (0 <= start < qubit_count and 0 <= target < qubit_count):
        raise ValueError(f"Qubit index out of range [0, {qubit_count - 1}].")

    if start == target:
        return 0

    adjacency: Dict[int, Set[int]] = {q: set() for q in range(qubit_count)}
    for a, b in processor.get("edges", []):
        u, v = int(a), int(b)
        adjacency[u].add(v)
        adjacency[v].add(u)

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        for neighbor in adjacency[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1  # Unconnected
