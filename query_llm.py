import csv
import requests


def read_csv(filename):
    """Reads a CSV file and returns a dictionary with 'Identifier / Formula' as keys and 'Name' as values."""
    data = {}
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            key = row['Identifier / Formula'].strip()
            value = row['Name'].strip()
            data[key] = value
    return data


def save_to_csv(data, filename, recommendations=None):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write headers
        headers = ["Identifier / Formula", "Name"]
        if recommendations:
            headers.extend([f"rank {i}" for i in range(1, 11)])
        writer.writerow(headers)

        # Write rows
        for key, value in data.items():
            row = [key, value]
            if recommendations and key in recommendations:
                row.extend(recommendations[key])
            writer.writerow(row)


def process_recommendations(identifiers_file, formulae_file):
    """Reads identifiers and formulae from CSV files, queries LLM, and saves recommendations."""
    # Read data from existing CSV files
    # identifiers = read_csv(identifiers_file)
    formulae = read_csv(formulae_file)

    # Query LLM and store recommendations
    identifier_recommendations = {}
    formula_recommendations = {}

    # for identifier, name in identifiers.items():
    #     recommendations = query_llm('Identifier', identifier)
    #     print(recommendations)
    #     ranked_recommendations = extract_recommendations(recommendations)
    #     identifier_recommendations[identifier] = ranked_recommendations

    for formula, name in formulae.items():
        recommendations = query_llm('Formula', formula)
        print(recommendations)
        ranked_recommendations = extract_recommendations(recommendations)
        formula_recommendations[formula] = ranked_recommendations

    # Save recommendations to new CSV files
    # save_to_csv(identifiers, 'data/identifiers_with_recommendations.csv',
    #             identifier_recommendations)
    save_to_csv(formulae, 'data/formulae_with_recommendations.csv',
                formula_recommendations)


def query_llm(prefix, input_text):
    """Queries the LLM with the given input text and returns the response."""
    url = 'http://localhost:11434/api/generate'

    prompt = f"""
    You are a mathematical formula/identifier recommender system. 
    Given a mathematical identifier or formula you provide a list of 10 possible recommendations for formula or identifier name. 
    Provide only the 10 names without further explanations. List these recommendations from most likely to least likely.
    Note: The identifiers or formulae are from the field of mathematics or physics. Choose the names accordingly based on popularity and usage in the field.

    Input:
    {prefix}: {input_text}
    """

    # Set headers and payload for the request
    headers = {'Content-Type': 'application/json'}
    payload = {"model": "llama3.1:8b", "prompt": prompt, "stream": False}

    print(prompt)
    response = requests.post(url, headers=headers, json=payload)

    return response.json().get(
        'response', "Sorry, I couldn't generate a response.")


def extract_recommendations(response):
    """Extracts the ranked recommendations from the LLM response."""
    recommendations = response.split("\n")
    ranked_recommendations = [
        line.split(". ", 1)[1].strip()
        for line in recommendations if line.strip().startswith(tuple(str(i) for i in range(1, 11)))
    ]
    return ranked_recommendations[:10]


if __name__ == "__main__":
    process_recommendations('data/identifiers.csv', 'data/formulae.csv')
