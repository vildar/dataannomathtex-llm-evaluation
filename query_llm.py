import requests
from utils import separate_identifiers_and_formulae
import csv


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


def process_identifiers_and_formulae(identifiers, formulae):
    # Separate identifiers and formulae into their respective CSVs
    save_to_csv(identifiers, 'identifiers.csv')
    save_to_csv(formulae, 'formulae.csv')

    # Query LLM and store recommendations
    # identifier_recommendations = {}
    # formula_recommendations = {}

    # for name, identifier in identifiers.items():
    #     recommendations = query_llm(identifier)
    #     ranked_recommendations = extract_recommendations(recommendations)
    #     identifier_recommendations[name] = ranked_recommendations

    # for formula, name in formulae.items():
    #     recommendations = query_llm(formula)
    #     ranked_recommendations = extract_recommendations(recommendations)
    #     formula_recommendations[formula] = ranked_recommendations

    # # Save recommendations to CSVs
    # save_to_csv(identifiers, 'identifiers_with_recommendations.csv', identifier_recommendations)
    # save_to_csv(formulae, 'formulae_with_recommendations.csv', formula_recommendations)


def query_llm(input_text):
    url = 'http://localhost:11434/api/generate'

    prompt = f"""
    You are a mathematical formula recommender system. Given a mathematical identifier or formula you provide a list of 10 possible recommendations for formula name. Provide only the 10 names without further explanations. List these recommendations from most likely to least likely.

    Input:
    {input_text}
    """

    # Set headers and payload for the request
    headers = {'Content-Type': 'application/json'}
    payload = {"model": "llama3.2:1b", "prompt": prompt, "stream": False}

    response = requests.post(url, headers=headers, json=payload)

    return response.json().get(
        'response', "Sorry, I couldn't generate a response.")


def extract_recommendations(response):
    # Extract the ranked recommendations from the response
    recommendations = response.split("\n")
    ranked_recommendations = [line.split(". ", 1)[1].strip()
                              for line in recommendations if ". " in line]
    return ranked_recommendations


if __name__ == "__main__":
    csv_file = 'cleaned_data.csv'
    identifiers_dict, formulae_dict = separate_identifiers_and_formulae(
        csv_file)
    process_identifiers_and_formulae(identifiers_dict, formulae_dict)
