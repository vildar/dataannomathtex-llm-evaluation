# Overview

This repository contains a set of Python scripts and utilities for processing mathematical identifiers and formulae, querying a local LLM (Large Language Model) API for recommendations, and generating CSV files with the processed data. The workflow involves separating identifiers and formulae from a dataset, querying the LLM for recommendations, and saving the results in structured CSV files.

## Prerequisites

- **Python**: Ensure Python 3.x is installed on your system.
- **Dependencies**: Install the required Python libraries by running:

  ```bash
  pip install -r requirements.txt
  ```

- **Local LLM API**: The scripts rely on a locally hosted LLM API. Ensure the API is running and accessible at the specified URL (`http://localhost:11434/api/generate`). Update the URL in the `query_llm.py` file if needed.

## Workflow

### 1. Input Data

The input data is stored in a CSV file located at `cleaned_data.csv`. This file contains two columns:

- **Identifier / Formula**: The mathematical identifier or formula.
- **Name**: The corresponding name or description.

### 2. Generating Identifiers and Formulae CSVs

The script `generate_identifier_formula_csv.py` processes the input data to separate identifiers and formulae into two separate CSV files:

- `data/identifiers.csv`
- `data/formulae.csv`

#### Steps:

Run the following command:

```bash
python generate_identifier_formula_csv.py
```

This script uses the `separate_identifiers_and_formulae` function from `utils.py` to classify each entry in `cleaned_data.csv` as either an identifier or a formula.

### 3. Querying the LLM for Recommendations

The script `query_llm.py` queries the local LLM API for recommendations based on the formulae in `data/formulae.csv`. The recommendations are saved in a new CSV file.

#### Steps:

1. Ensure the local LLM API is running at `http://localhost:11434/api/generate`.
2. Run the following command:

   ```bash
   python query_llm.py
   ```

The script performs the following:

- Reads the formulae from `data/formulae.csv`.
- Sends each formula to the LLM API using the `query_llm` function.
- Extracts the top 10 recommendations using the `extract_recommendations` function.
- Saves the results in `data/formulae_with_recommendations.csv`.

### 4. Automating the Workflow

The `build.sh` script automates the entire process. It supports two modes:

- **create**: Generates `identifiers.csv` and `formulae.csv` from `cleaned_data.csv`.
- **rank**: Queries the LLM and generates recommendations.

#### Steps:

Run the script with the desired mode:

```bash
bash build.sh create
bash build.sh rank
```

Ensure the script has executable permissions:

```bash
chmod +x build.sh
```

## Caveats

- **Local LLM API**: The scripts rely on a locally hosted LLM API. Ensure the API is running and accessible at the specified URL (`http://localhost:11434/api/generate`). If the API URL changes, update the `query_llm.py` file accordingly.
- **Input Data Format**: The input CSV (`data/cleaned_data.csv`) must have the columns `Identifier / Formula` and `Name` for the scripts to function correctly.

## Example Usage

### Generate `identifiers.csv` and `formulae.csv`:

```bash
python generate_identifier_formula_csv.py
```

### Query the LLM for recommendations:

```bash
python query_llm.py
```

### View the generated files:

- `data/identifiers.csv`
- `data/formulae.csv`
- `data/formulae_with_recommendations.csv`
- `data/identifiers_with_recommendations.csv`

## License

This project is licensed under the MIT License.
