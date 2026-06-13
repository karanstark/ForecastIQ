import pandas as pd
import joblib
import os
import argparse
from lightgbm import LGBMRegressor

from preprocess import load_and_preprocess
from generate_features import engineer_features

def train_models(data_dir: str, model_path: str):
    print("Loading data...")
    df = load_and_preprocess(data_dir)
    print("Engineering features...")
    df = engineer_features(df)
    
    features = ['Spend', 'Clicks', 'Impressions', 'CTR', 'ConversionRate', 'DayOfWeek', 'Month', 'Revenue_Rolling_7', 'Spend_Rolling_7', 'Revenue_Rolling_30', 'Spend_Rolling_30']
    
    train_df = df[df['Spend'] > 0]
    
    if len(train_df) < 5:
        print("Not enough data to train.")
        return
        
    X = train_df[features]
    y_rev = train_df['Revenue']
    y_roas = train_df['ROAS']
    
    print("Training LightGBM models...")
    rev_model = LGBMRegressor(random_state=42, n_estimators=100)
    roas_model = LGBMRegressor(random_state=42, n_estimators=100)
    
    rev_model.fit(X, y_rev)
    roas_model.fit(X, y_roas)
    
    models = {
        'revenue': rev_model,
        'roas': roas_model,
        'features': features
    }
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(models, model_path)
    print(f"Models saved to {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--model_path', type=str, default='pickle/model.pkl')
    args = parser.parse_args()
    
    train_models(args.data_dir, args.model_path)
