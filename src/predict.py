import pandas as pd
import joblib
import os
import argparse

from preprocess import load_and_preprocess
from generate_features import engineer_features

def predict(data_dir: str, model_path: str, output_path: str):
    print("Loading recent data...")
    df = load_and_preprocess(data_dir)
    df = engineer_features(df)
    
    predictions = []
    latest = df.groupby('Channel').tail(1).copy()
    
    try:
        print("Loading ML model...")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}.")
            
        models = joblib.load(model_path)
        rev_model = models['revenue']
        roas_model = models['roas']
        features = models['features']
        
        print("Generating ML predictions...")
        
        for index, row in latest.iterrows():
            # Predict next 30 days based on latest features
            synth_X = pd.DataFrame([row[features]] * 30)
            rev_preds = rev_model.predict(synth_X)
            roas_preds = roas_model.predict(synth_X)
            
            predictions.append({
                'Channel': row['Channel'],
                'Forecast_Period': '30_days',
                'Forecast_Revenue': rev_preds.sum(),
                'Forecast_ROAS': roas_preds.mean()
            })
            
    except Exception as e:
        print(f"ML Model failed with error: {e}")
        print("ACTIVATING BACKUP PLAN: Falling back to heuristic rolling averages to guarantee output.")
        
        # Backup Plan: Use the 30-day historical averages to project the next 30 days
        for channel in df['Channel'].unique():
            channel_df = df[df['Channel'] == channel].tail(30)
            avg_daily_rev = channel_df['Revenue'].mean()
            avg_daily_spend = channel_df['Spend'].mean()
            
            # If spend is 0, avoid division by zero
            fallback_roas = (avg_daily_rev / avg_daily_spend) if avg_daily_spend > 0 else 0
            
            predictions.append({
                'Channel': channel,
                'Forecast_Period': '30_days',
                'Forecast_Revenue': avg_daily_rev * 30, # Project 30 days
                'Forecast_ROAS': fallback_roas
            })
            
    out_df = pd.DataFrame(predictions)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out_df.to_csv(output_path, index=False)
    print(f"Predictions successfully saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    parser.add_argument('model_path', type=str)
    parser.add_argument('output_path', type=str)
    args = parser.parse_args()
    
    predict(args.data_dir, args.model_path, args.output_path)
