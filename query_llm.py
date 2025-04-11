import requests
from utils import separate_identifiers_and_formulae


def query_llm(formula):
    url = 'http://localhost:11434/api/generate'

    prompt = f"""
    You are an expert in mathematical annotation recommendation.

    Task:
    Given a mathematical formula or identifier, provide **10 ranked recommendations** for **formula names** from most likely to least likely. 
    Do not provide explanations of the formula. or additional steps. Just provide the ranked list of formula names or identifiers. 
    Each recommendation should be a **relevant formula name or identifier**.

    Format your response as follows:
    1. <Most relevant formula name or identifier>
    2. <Second most relevant formula name or identifier>
    ...
    10. <Least relevant formula name or identifier>

    Formula/Identifier to analyze:
    {formula}
    """

    # Set headers and payload for the request
    headers = {'Content-Type': 'application/json'}
    payload = {"model": "llama3.2:1b", "prompt": prompt, "stream": False}

    response = requests.post(url, headers=headers, json=payload)

    return response.json().get(
        'response', "Sorry, I couldn't generate a response.")


if __name__ == "__main__":
    csv_file = 'cleaned_data.csv'
    identifiers_dict, formulae_dict = separate_identifiers_and_formulae(
        csv_file)
    # formula = "E = mc^2"
    # recommendations = query_llm(formula)
    # print("Recommendations:")
    # print(recommendations)
