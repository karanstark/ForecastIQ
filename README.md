# ForecastIQ

**AI-Assisted Probabilistic Revenue & ROAS Forecasting Platform for E-commerce Marketing Agencies**


## Overview
ForecastIQ evaluates historical e-commerce campaign datasets (Google Ads, Meta Ads, Bing Ads) to generate rolling future revenue and Return on Ad Spend (ROAS) predictions using a robust LightGBM machine learning pipeline.

This repository is optimized for **automated CLI evaluation**.

## Structure

```text
ForecastIQ/
├── run.sh                          # Main evaluation entry point
├── requirements.txt                # Python dependencies
├── data/                           # Directory containing input CSVs
├── pickle/                         # Directory containing the pre-trained LightGBM model
├── output/                         # Directory where predictions.csv will be saved
└── src/                            # Core ML source code
    ├── preprocess.py               # Data ingestion & normalization
    ├── generate_features.py        # Feature engineering (CTR, ROAS, Rolling Avgs)
    ├── train.py                    # Model training logic
    ├── predict.py                  # CLI prediction logic
    └── utils.py                    # Mock data generators
```

## Setup Instructions
```bash
# 1. Clone the repository
git clone https://github.com/karanstark/ForecastIQ.git
cd ForecastIQ

# 2. Install dependencies
pip install -r requirements.txt
```

> Evaluation note: The judged pipeline runs entirely through `run.sh`. Do not require notebooks, prompts, or network calls during evaluation.

## Running the Evaluation Pipeline

The primary method for interacting with this prototype is via the automated `run.sh` script.
This script guarantees 100% offline, reproducible execution without relying on external API keys or networks.

### Execution
```bash
./run.sh ./data ./pickle/model.pkl ./output/predictions.csv
```

> This command must execute non-interactively and produce `predictions.csv` without any runtime network calls.

### Expected Output
The script will read the unified historical datasets from `data/`, load the pre-trained LightGBM model from `pickle/model.pkl`, and output a formatted `predictions.csv` directly into the `output/` directory.

The `predictions.csv` includes:
- `Channel`
- `Forecast_Period`
- `Forecast_Revenue`
- `Forecast_ROAS`
