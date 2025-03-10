from sympy import primerange
import itertools
import matplotlib.pyplot as plt
import networkx as nx

# Define mapping of primes to vowels
prime_to_vowel = {
    1: 'A',
    2: 'E',
    3: 'I',
    5: 'O',
    7: 'U'
}

# Function to generate the vowel representation of a prime number
# Extend this mapping using the corresponding first primes to their respective vowels
def prime_to_vowel_string(primes):
    return [prime_to_vowel.get(p, '?') for p in primes]

# Generate prime numbers in a range and apply vowel mapping
def generate_vowel_mappings(limit):
    primes = list(primerange(1, limit))  # Generate prime numbers up to 'limit'
    vowel_mappings = prime_to_vowel_string(primes) 
    return primes, vowel_mappings

# Define a function to compute composite values and map them to vowel 
representations
def composite_vowel_mapping(primes, vowel_mappings):
    composites = []
    composite_mappings = []
    
    # Generate composites by multiplying each pair of primes
    for (p1, v1), (p2, v2) in itertools.combinations(zip(primes, vowel_mappings), 2):
        composite = p1 * p2
        composites.append(composite)
        # Use the lowercase-uppercase rule for distinguishing factor order
        mapping = v1.lower() + v2.upper() if p1 < p2 else v2.lower() + v1.upper()
        composite_mappings.append(mapping)
    return composites, composite_mappings

# Define a visualization of vowel mappings
# (for simplicity, just print them here)
def visualize_vowel_patterns(primes, vowel_mappings, composites, 
composite_mappings):
    print("Prime Vowel Mapping:")
    for prime, vowel in zip(primes, vowel_mappings):
        print(f"{prime} -> {vowel}")
    
    print("\nComposite Vowel Mapping:")
    for composite, mapping in zip(composites, composite_mappings):
        print(f"{composite} -> {mapping}")

# Plotting the prime and composite relationships using a graph
def plot_vowel_graph(primes, vowel_mappings, composites, 
composite_mappings):
    G = nx.Graph()
    
    # Add nodes for primes
    for prime, vowel in zip(primes, vowel_mappings):
        G.add_node(prime, label=vowel)
    
    # Add edges for composites
    for (p1, p2), mapping in zip(itertools.combinations(primes, 2), 
composite_mappings):
        composite = p1 * p2
        G.add_edge(p1, p2, label=mapping)
    
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, 
node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
font_color='red')
    

