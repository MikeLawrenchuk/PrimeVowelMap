from sympy import primerange, factorint
import itertools
import matplotlib.pyplot as plt
import networkx as nx

# Define mapping of primes to vowels (extended to avoid '?')
prime_to_vowel = {
    1: 'A',
    2: 'E',
    3: 'I',
    5: 'O',
    7: 'U'
}

# Fallback vowels to be used for higher primes
fallback_vowels = ['A', 'E', 'I', 'O', 'U']

# Function to generate the vowel representation of a prime number
# Extend this mapping using the corresponding first primes to their respective vowels
def prime_to_vowel_string(primes):
    vowels = []
    for p in primes:
        if p in prime_to_vowel:
            vowels.append(prime_to_vowel[p])
        else:
            # Use fallback vowels in a repeating manner for higher primes
            index = (p % len(fallback_vowels)) - 1
            vowels.append(fallback_vowels[index])
    return vowels

# Generate prime numbers in a range and apply vowel mapping
def generate_vowel_mappings(limit):
    primes = list(primerange(1, limit))  # Generate prime numbers up to 'limit'
    vowel_mappings = prime_to_vowel_string(primes)
    return primes, vowel_mappings

# Define a function to compute composite values and map them to vowel representations
# Also define specific mappings for primes like 11 = 'AA' and 13 = 'AI'
def composite_vowel_mapping(primes, vowel_mappings):
    composites = []
    composite_mappings = []
    
    # Special cases for direct prime vowel combinations
    special_prime_mappings = {
        11: 'AA',
        13: 'AI'
    }
    
    # Generate composites by considering addition, multiplication, and exponentiation for each pair of primes
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
            composites.append(composite_exp)
            composite_mappings.append(v1.upper() + v2.lower() + " (Exponentiation)")
        else:
            composite_exp = p2 ** p1
            composites.append(composite_exp)
            composite_mappings.append(v2.upper() + v1.lower() + " (Exponentiation)")

    return composites, composite_mappings

# Define a visualization of vowel mappings
# (for simplicity, just print them here)
def visualize_vowel_patterns(primes, vowel_mappings, composites, composite_mappings):
    print("Prime Vowel Mapping:")
    for prime, vowel in zip(primes, vowel_mappings):
        print(f"{prime} -> {vowel}")
    
    print("\nComposite Vowel Mapping:")
    for composite, mapping in zip(composites, composite_mappings):
        print(f"{composite} -> {mapping}")

# Plotting the prime and composite relationships using an interactive graph with Plotly
import plotly.graph_objs as go
import plotly.io as pio

def plot_vowel_graph(primes, vowel_mappings, composites, composite_mappings):
    G = nx.Graph()
    
    # Add nodes for primes
    for prime, vowel in zip(primes, vowel_mappings):
        # Determine color based on the last digit of the prime
        last_digit = prime % 10
        if last_digit == 1:
            node_color = 'red'
        elif last_digit == 3:
            node_color = 'blue'
        elif last_digit == 7:
            node_color = 'green'
        elif last_digit == 9:
            node_color = 'purple'
        else:
            node_color = 'skyblue'  # Default color for any other last digit
        G.add_node(prime, label=vowel, color=node_color)
    
    # Add edges for composites
    for (p1, p2), mapping in zip(itertools.combinations(primes, 2), composite_mappings):
        # Determine the type of edge based on the operation in the mapping
        composite = None
        if "(Sum)" in mapping:
            composite = p1 + p2
            edge_style = 'solid'
            edge_color = 'blue'
        elif "(Product)" in mapping:
            composite = p1 * p2
            edge_style = 'dashed'
            edge_color = 'red'
        elif "(Exponentiation)" in mapping:
            composite = p1 ** p2 if p1 < p2 else p2 ** p1
            edge_style = 'dotted'
            edge_color = 'green'
        G.add_edge(p1, p2, label=mapping, color=edge_color)
    
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
    node_color = []
    for node in G.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node[0]} ({node[1]['label']})")
        node_color.append(node[1]['color'])
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            size=10,
            color=node_color,
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
    pio.show(fig)

# Function to find the prime factors of a number
def find_prime_factors(number):
    factors = factorint(number)
    print(f"Prime factors of {number}:")
    for prime, power in factors.items():
        print(f"{prime}^{power}")
    return factors

# Main function to execute the exploration
def main():
    limit = 20  # Set limit to generate primes within a range
    primes, vowel_mappings = generate_vowel_mappings(limit)
    composites, composite_mappings = composite_vowel_mapping(primes, vowel_mappings)
    visualize_vowel_patterns(primes, vowel_mappings, composites, composite_mappings)
    
    # Example of finding prime factors before plotting
    number_to_factor = int(input("Enter a number to find its prime factors: "))
    find_prime_factors(number_to_factor)
    
    # Plot the graph after factoring
    plot_vowel_graph(primes, vowel_mappings, composites, composite_mappings)

if __name__ == "__main__":
    main()
