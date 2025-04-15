import requests
from utils import separate_identifiers_and_formulae
import csv


def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write headers
        headers = ["Identifier / Formula", "Name"]
        writer.writerow(headers)

        # Write rows
        for key, value in data.items():
            row = [key, value]
            writer.writerow(row)


if __name__ == "__main__":
    csv_file = 'cleaned_data.csv'
    identifiers_dict, formulae_dict = separate_identifiers_and_formulae(
        csv_file)
    save_to_csv(identifiers_dict, 'identifiers.csv')
    save_to_csv(formulae_dict, 'formulae.csv')
