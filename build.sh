#!/bin/bash

MODE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --mode) MODE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

case $MODE in
    create)
        echo "Running generate_identifier_formula_csv.py..."
        python3 generate_identifier_formula_csv.py
        ;;
    rank)
        echo "Running query_llm.py..."
        python3 query_llm.py
        ;;
    *)
        echo "Invalid mode. Use --mode create|rank"
        exit 1
        ;;
esac
