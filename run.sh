#!/bin/bash

# CLI arguments
DATA_DIR=$1
MODEL_PATH=$2
OUTPUT_PATH=$3

if [ "$#" -ne 3 ]; then
    echo "Usage: ./run.sh <data_dir> <model_path> <output_path>"
    exit 1
fi

echo "Running ForecastIQ Evaluation Pipeline..."

# Execute prediction
python src/predict.py "$DATA_DIR" "$MODEL_PATH" "$OUTPUT_PATH"

if [ $? -eq 0 ]; then
    echo "Evaluation complete. Output written to $OUTPUT_PATH"
else
    echo "Primary pipeline failed — invoking pure-Python backup predictor..."
    python src/backup_predict.py "$DATA_DIR" "$OUTPUT_PATH"
    if [ $? -eq 0 ]; then
        echo "Backup predictor succeeded. Output written to $OUTPUT_PATH"
    else
        echo "Backup predictor failed. Pipeline failed." 
        exit 1
    fi
fi
