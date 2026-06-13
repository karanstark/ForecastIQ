# System Architecture

## Core Philosophy
The architecture is designed specifically to prioritize **reliability, speed, and reproducibility** in a zero-network sandbox environment.

## 1. Machine Learning Pipeline (LightGBM)
We transitioned from an ensemble approach to a single **LightGBM Regressor** model to maximize speed, minimize pickle size, and guarantee flawless automated evaluation.

### Feature Engineering
- **Schema Unification:** Merges mismatched schemas from Google, Meta, and Bing CSVs into a strict 8-column format.
- **Rolling Averages:** Generates 7-day and 30-day lookback windows for Spend and Revenue.
- **Derived Metrics:** Computes synthetic metrics such as CTR, Conversion Rate, and historical ROAS.

### Execution Flow (`run.sh`)
1. **`src/predict.py`**: Invoked with data, model, and output paths.
2. **`src/preprocess.py`**: Reads and cleans CSVs.
3. **`src/generate_features.py`**: Appends ML-ready features.
4. **LightGBM**: Loads `pickle/model.pkl`, predicts the next 30 days.
5. **Output**: Writes the combined `predictions.csv` directly to the specified path.

## 2. CI/CD Pipeline
- **Source Control:** GitHub
- **Continuous Integration:** GitHub Actions runs `bash run.sh ./data ./pickle/model.pkl ./output/predictions.csv` on every push to verify the core pipeline never breaks.
