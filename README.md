# Prime Vowel Mapping Project

## Description
This project explores relationships between prime numbers by mapping them 
to vowel representations. The script performs the following tasks:
- Maps prime numbers to vowels.
- Generates composites from primes using different operations (addition, 
multiplication, exponentiation).
- Visualizes relationships between primes and composites using an 
interactive graph.
- Allows users to find the prime factors of a number.

## Features
1. **Prime to Vowel Mapping**: Primes are mapped to vowels (A, E, I, O, U) 
and extended using fallback vowels for higher primes.
2. **Composite Generation**: Composite numbers are generated from pairs of 
primes using addition, multiplication, and exponentiation.
3. **Interactive Visualization**: The relationships are plotted using 
Plotly, allowing for interactive exploration.
4. **Prime Factorization**: Users can enter a number to find its prime 
factors using the `factorint` method from SymPy.

## Usage
1. **Run the Script**: To execute the project, simply run the 
`prime-vowel.py` file.
   ```bash
   python prime-vowel.py
   ```
2. **Enter a Number**: When prompted, enter a number to find its prime 
factors.
3. **Interactive Graph**: After factoring, an interactive graph is 
displayed showing relationships between prime numbers and their 
composites.

## Dependencies
- `sympy`: Used for generating primes and factorizing numbers.
- `matplotlib`: Used for plotting (although now enhanced with Plotly).
- `networkx`: Used for creating the graph structure.
- `plotly`: Used for interactive visualization of the prime-composite 
relationships.

## Installation
To install the necessary dependencies, run:
```bash
pip install sympy matplotlib networkx plotly
```

## Example
- The script generates prime numbers up to a limit (`limit = 20` by 
default).
- Each prime is mapped to a vowel.
- Pairs of primes are used to create composite values using addition, 
multiplication, and exponentiation.
- The relationships are visualized using an interactive Plotly graph.

## Project Files
- **`prime-vowel.py`**: The main script to run the project.
- **`.gitignore`**: Used to ignore unnecessary system files like 
`.DS_Store`.

## How to Contribute
If you want to contribute to this project, feel free to fork the 
repository and submit a pull request.
