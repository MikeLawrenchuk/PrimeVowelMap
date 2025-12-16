# Prime Vowel Mapping Project

import itertools
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio
from sympy import factorint, primerange

# Define mapping of the first few primes to vowels. Remaining primes reuse
# vowels in order to keep the mapping readable for large ranges.
prime_to_vowel = {
    2: "A",
    3: "E",
    5: "I",
    7: "O",
    11: "U",
}

fallback_vowels = ["A", "E", "I", "O", "U", "Y"]


@dataclass
class CompositeMapping:
    """Represents a single composite derived from two primes."""

    primes: Tuple[int, int]
    operation: str
    value: int
    label: str


def prime_to_vowel_string(primes: Iterable[int]) -> List[str]:
    """Map primes to vowel strings, cycling through a fallback list if needed."""

    vowels: List[str] = []
    for index, prime in enumerate(primes):
        vowels.append(prime_to_vowel.get(prime, fallback_vowels[index % len(fallback_vowels)]))
    return vowels

# Generate prime numbers in a range and apply vowel mapping
def generate_vowel_mappings(limit: int) -> Tuple[List[int], List[str]]:
    """Generate primes and their corresponding vowel mappings."""

    primes = list(primerange(2, limit))
    vowel_mappings = prime_to_vowel_string(primes)
    return primes, vowel_mappings

# Define a function to compute composite values and map them to vowel representations
def generate_composite_vowel_mappings(
    primes: List[int], vowel_mappings: List[str]
) -> Tuple[List[int], List[CompositeMapping]]:
    """
    Generate composites and their vowel mappings based on prime operations.

    Returns both the raw composite numbers and richer mapping metadata so that
    visualizations have a one-to-one correspondence with the generated values.
    """

    composites: List[int] = []
    composite_mappings: List[CompositeMapping] = []

    for (p1, v1), (p2, v2) in itertools.combinations(zip(primes, vowel_mappings), 2):
        composites, composite_mappings = _add_composites_for_pair(
            p1, p2, v1, v2, composites, composite_mappings
        )

    return composites, composite_mappings


def _add_composites_for_pair(
    p1: int,
    p2: int,
    v1: str,
    v2: str,
    composites: List[int],
    composite_mappings: List[CompositeMapping],
) -> Tuple[List[int], List[CompositeMapping]]:
    """Add composites for a pair of primes and return the augmented collections."""

    operations: Dict[str, Tuple[int, str]] = {
        "Sum": (p1 + p2, f"{v1.upper()}{v2.upper()}"),
        "Product": (p1 * p2, f"{v1.lower()}{v2.upper()}"),
        "Exponentiation": (
            p1**p2 if p1 < p2 else p2**p1,
            f"{v1.upper()}{v2.lower()}",
        ),
    }

    for operation, (value, label) in operations.items():
        composites.append(value)
        composite_mappings.append(
            CompositeMapping(primes=tuple(sorted((p1, p2))), operation=operation, value=value, label=label)
        )

    return composites, composite_mappings

# Visualize vowel patterns
def visualize_vowel_patterns(
    primes: List[int], vowel_mappings: List[str], composites: List[int], composite_mappings: List[CompositeMapping]
) -> None:
    """Display the mappings between primes, composites, and vowels."""

    print("Prime Vowel Mapping:")
    for prime, vowel in zip(primes, vowel_mappings):
        print(f"{prime} -> {vowel}")

    print("\nComposite Vowel Mapping:")
    for composite, mapping in zip(composites, composite_mappings):
        print(f"{composite} -> {mapping.label} ({mapping.operation})")

# Plot vowel graph using Plotly
def plot_vowel_graph(
    primes: List[int],
    vowel_mappings: List[str],
    composite_mappings: List[CompositeMapping],
) -> None:
    """Plot an interactive graph showing prime and composite relationships."""

    G = nx.Graph()

    for prime, vowel in zip(primes, vowel_mappings):
        G.add_node(prime, label=vowel)

    edge_labels = _aggregate_edge_labels(composite_mappings)
    for (p1, p2), label in edge_labels.items():
        G.add_edge(p1, p2, label=label)

    pos = nx.spring_layout(G)
    edge_x: List[float] = []
    edge_y: List[float] = []
    edge_text: List[str] = []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(data["label"])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="gray"),
        hoverinfo="text",
        mode="lines",
        text=edge_text,
    )

    node_x: List[float] = []
    node_y: List[float] = []
    node_text: List[str] = []
    for node, data in G.nodes(data=True):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node} ({data['label']})")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        marker=dict(size=10, color="blue", line_width=2),
        text=node_text,
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Interactive Prime and Composite Vowel Graph",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    pio.write_html(fig, file="vowel_graph.html", auto_open=True)

# Find prime factors of a number
def find_prime_factors(number: int) -> Dict[int, int]:
    """
    Find prime factors of a number.

    Parameters:
        number (int): The number to factorize.

    Returns:
        dict: Dictionary of prime factors and their powers.
    """
    factors = factorint(number)
    print(f"Prime factors of {number}:")
    for prime, power in factors.items():
        print(f"{prime}^{power}")
    return factors

# Static plot with Matplotlib
def plot_static_graph(
    primes: List[int], vowel_mappings: List[str], composite_mappings: List[CompositeMapping]
) -> None:
    """Plot a static graph of prime and composite relationships using Matplotlib."""

    G = nx.Graph()
    for prime, vowel in zip(primes, vowel_mappings):
        G.add_node(prime, label=vowel)

    edge_labels = _aggregate_edge_labels(composite_mappings)
    for (p1, p2), label in edge_labels.items():
        G.add_edge(p1, p2, label=label)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, "label")
    edge_labels = nx.get_edge_attributes(G, "label")

    plt.figure(figsize=(10, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_size=700,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        edge_color="gray",
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.show()

# Main function
def main() -> None:
    try:
        limit = int(input("Enter the upper limit for prime generation: "))
        if limit <= 2:
            raise ValueError("Limit must be an integer greater than 2.")

        primes, vowel_mappings = generate_vowel_mappings(limit)
        composites, composite_mappings = generate_composite_vowel_mappings(primes, vowel_mappings)
        visualize_vowel_patterns(primes, vowel_mappings, composites, composite_mappings)

        number_to_factor = int(input("Enter a number to find its prime factors: "))
        find_prime_factors(number_to_factor)

        visualization_choice = input("Choose visualization (static/interactive): ").strip().lower()
        if visualization_choice == "static":
            plot_static_graph(primes, vowel_mappings, composite_mappings)
        elif visualization_choice == "interactive":
            plot_vowel_graph(primes, vowel_mappings, composite_mappings)
        else:
            print("Invalid choice. Skipping visualization.")

    except ValueError as e:
        print(f"Invalid input: {e}")


def _aggregate_edge_labels(composite_mappings: List[CompositeMapping]) -> Dict[Tuple[int, int], str]:
    """Combine composite mappings for each prime pair into a readable label."""

    edge_labels: Dict[Tuple[int, int], List[str]] = {}
    for mapping in composite_mappings:
        edge_labels.setdefault(mapping.primes, []).append(
            f"{mapping.label} ({mapping.operation}: {mapping.value})"
        )

    return {primes: "\n".join(labels) for primes, labels in edge_labels.items()}

if __name__ == "__main__":
    main()
