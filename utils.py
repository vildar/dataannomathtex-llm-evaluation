import csv
import re


def is_latex_formula(value):
    # LaTeX formulas typically include math symbols, like \alpha, \frac{}, \sum, etc.
    # We'll look for common LaTeX math expressions such as backslashes or math operators
    # Looks for LaTeX commands or math operators
    latex_formula_pattern = re.compile(r'[\\\+\-\*/^=<>()]|{[^}]*}')
    return bool(latex_formula_pattern.search(value))

# Function to separate identifiers and formulae


def separate_identifiers_and_formulae(csv_file):
    identifiers = {}
    formulae = {}

    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Assuming column name is "Identifier / Formula"
            value = row['Identifier / Formula'].strip()

            if is_latex_formula(value):
                formulae[value] = 0
            else:
                identifiers[value] = 0

    return identifiers, formulae
