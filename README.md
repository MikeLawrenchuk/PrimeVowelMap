# Prime Vowel Mapping Project

A Python program that maps prime numbers to vowels, generates composites through mathematical operations, and visualizes the relationships using graphs. It also includes utilities for prime factorization.

---

## Features
- **Prime-to-Vowel Mapping**: Assigns vowels to prime numbers and dynamically maps higher primes using fallback vowels.
- **Composite Generation**: Creates composite numbers through addition, multiplication, and exponentiation of prime pairs.
- **Visualization**:
  - Static graphs using Matplotlib.
  - Interactive graphs using Plotly.
- **Prime Factorization**: Identifies the prime factors of a given number.

---

## Requirements
The program requires the following Python packages:

```bash
sympy==1.13.3
matplotlib==3.9.2
networkx==3.4.2
plotly==5.24.1
```

To install dependencies, run:

```bash
pip install -r requirements.txt
```

---

## How to Run
1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd PrimeVowelMap
   ```

2. Run the program:

   ```bash
   python prime_vowel_map.py
   ```

3. Follow the on-screen prompts:
   - Enter an upper limit for generating primes.
   - Enter a number to factorize.
   - Choose a visualization method (static or interactive).

---

## Example Usage
**Input**:
- Upper limit for primes: `20`
- Number to factorize: `30`
- Visualization: `static`

**Output**:
- A list of primes and their vowel mappings.
- Composite mappings based on mathematical operations.
- Prime factors of the input number.
- A graph visualizing relationships (static or interactive).

---

## Functions
1. `generate_vowel_mappings(limit)`:
   - Generates prime numbers up to the specified limit and maps them to vowels.

2. `generate_composite_vowel_mappings(primes, vowel_mappings)`:
   - Creates composites using addition, multiplication, and exponentiation.

3. `plot_static_graph(primes, vowel_mappings, composites, composite_mappings)`:
   - Visualizes relationships using Matplotlib.

4. `plot_vowel_graph(primes, vowel_mappings, composites, composite_mappings)`:
   - Visualizes relationships interactively using Plotly.

5. `find_prime_factors(number)`:
   - Finds the prime factors of a given number.

---

## Limitations
- Large values for prime generation or exponentiation may cause performance issues.
- Requires Python 3.8+ for compatibility.

---

## Future Enhancements
- Optimize composite generation for larger numbers.
- Add support for distributed computation of primes and composites.
- Improve graph aesthetics for better clarity with large datasets.

