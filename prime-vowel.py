# Prime Vowel Mapping Project

from sympy import primerange, factorint
# from debug_utilities import debug_all
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio

# Define mapping of primes to vowels (extended to avoid '?')
prime_to_vowel = {
    1: 'A',  # Last digit of some primes
    3: 'I',  # Last digit of some primes
    7: 'U',  # Last digit of some primes
    9: 'O'   # Last digit of some primes (though less common)
}

fallback_vowels = ['A', 'E', 'I', 'O', 'U', 'Y']

# Function to map a single prime number to a vowel
def map_prime_to_vowel(prime):
    # Extract the last digit of the prime number
    last_digit = prime % 10
    
    # Check if there's a direct mapping for the last digit
    if last_digit in prime_to_vowel:
        return prime_to_vowel[last_digit]
    else:
        # Use fallback vowels in a cyclic manner
        index = (prime % len(fallback_vowels))
        return fallback_vowels[index]


# Function to generate the vowel representation of a prime number
def prime_to_vowel_string(primes):
    """
    Map primes to vowel strings, with fallback for higher primes.

    Parameters:
        primes (list): List of prime numbers.

    Returns:
        list: List of corresponding vowels.
    """
    vowels = []
    for p in primes:
        if p in prime_to_vowel:
            vowels.append(prime_to_vowel[p])
        else:
            index = (p % len(fallback_vowels))
            vowels.append(fallback_vowels[index])
    return vowels

# Generate prime numbers in a range and apply vowel mapping
def generate_vowel_mappings(limit):
    """
    Generate primes and their corresponding vowel mappings.

    Parameters:
        limit (int): Upper limit for prime generation.

    Returns:
        tuple: List of primes and their vowel mappings.
    """
    primes = list(primerange(1, limit))
    vowel_mappings = prime_to_vowel_string(primes)
    return primes, vowel_mappings

# Define a function to compute composite values and map them to vowel representations
def generate_composite_vowel_mappings(primes, vowel_mappings):
    """
    Generate composites and their vowel mappings based on prime operations.

    Parameters:
        primes (list): List of prime numbers.
        vowel_mappings (list): Corresponding vowel mappings.

    Returns:
        tuple: List of composites and their mappings.
    """
    composites = []
    composite_mappings = []

    for (p1, v1), (p2, v2) in itertools.combinations(zip(primes, vowel_mappings), 2):
        # Addition
        composite_sum = p1 + p2
        composites.append(composite_sum)
        composite_mappings.append(v1.upper() + v2.upper() + " (Sum)")

        # Multiplication
        composite_product = p1 * p2
        composites.append(composite_product)
        composite_mappings.append(v1.lower() + v2.upper() + " (Product)")

        # Exponentiation (smaller prime raised to larger prime)
        if p1 < p2:
            composite_exp = p1 ** p2
        else:
            composite_exp = p2 ** p1
        composites.append(composite_exp)
        composite_mappings.append(v1.upper() + v2.lower() + " (Exponentiation)")

    return composites, composite_mappings

# Visualize vowel patterns
def visualize_vowel_patterns(primes, vowel_mappings, composites, composite_mappings):
    """
    Display the mappings between primes, composites, and vowels.

    Parameters:
        primes (list): List of prime numbers.
        vowel_mappings (list): Corresponding vowel mappings.
        composites (list): List of composite numbers.
        composite_mappings (list): Corresponding composite mappings.
    """
    print("Prime Vowel Mapping:")
    for prime, vowel in zip(primes, vowel_mappings):
        print(f"{prime} -> {vowel}")

    print("\nComposite Vowel Mapping:")
    for composite, mapping in zip(composites, composite_mappings):
        print(f"{composite} -> {mapping}")

# Plot vowel graph using Plotly
def plot_vowel_graph(primes, vowel_mappings, composites, composite_mappings):
    """
    Plot an interactive graph showing prime and composite relationships.

    Parameters:
        primes (list): List of prime numbers.
        vowel_mappings (list): Corresponding vowel mappings.
        composites (list): List of composite numbers.
        composite_mappings (list): Corresponding composite mappings.
    """
    G = nx.Graph()

    # Add nodes for primes
    for prime, vowel in zip(primes, vowel_mappings):
        G.add_node(prime, label=vowel)

    # Add edges for composites
    for (p1, p2), mapping in zip(itertools.combinations(primes, 2), composite_mappings):
        G.add_edge(p1, p2, label=mapping)

    # Convert NetworkX graph to Plotly format
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    edge_text = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(edge[2]['label'])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='gray'),
        hoverinfo='text',
        mode='lines',
        text=edge_text
    )

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node[0]} ({node[1]['label']})")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            size=10,
            color='blue',
            line_width=2
        ),
        text=node_text
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='Interactive Prime and Composite Vowel Graph',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                 ))
       
    # Save and open in a web browser
    pio.write_html(fig, file='vowel_graph.html', auto_open=True)

# Find prime factors of a number
def find_prime_factors(number):
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
def plot_static_graph(primes, vowel_mappings, composites, composite_mappings):
    """
    Plot a static graph of prime and composite relationships using Matplotlib.

    Parameters:
        primes (list): List of prime numbers.
        vowel_mappings (list): Corresponding vowel mappings.
        composites (list): List of composite numbers.
        composite_mappings (list): Corresponding composite mappings.
    """
    G = nx.Graph()
    for prime, vowel in zip(primes, vowel_mappings):
        G.add_node(prime, label=vowel)

    for (p1, p2), mapping in zip(itertools.combinations(primes, 2), composite_mappings):
        G.add_edge(p1, p2, label=mapping)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.show()

# Main function
def main():
    try:
        limit = int(input("Enter the upper limit for prime generation: "))
        if limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        primes, vowel_mappings = generate_vowel_mappings(limit)
        composites, composite_mappings = generate_composite_vowel_mappings(primes, vowel_mappings)
        visualize_vowel_patterns(primes, vowel_mappings, composites, composite_mappings)

        number_to_factor = int(input("Enter a number to find its prime factors: "))
        find_prime_factors(number_to_factor)

        visualization_choice = input("Choose visualization (static/interactive): ").strip().lower()
        if visualization_choice == 'static':
            plot_static_graph(primes, vowel_mappings, composites, composite_mappings)
        elif visualization_choice == 'interactive':
            plot_vowel_graph(primes, vowel_mappings, composites, composite_mappings)
        else:
            print("Invalid choice. Skipping visualization.")

    except ValueError as e:
        print(f"Invalid input: {e}")

if __name__ == "__main__":
    main()
