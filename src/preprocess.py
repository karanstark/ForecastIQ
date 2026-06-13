import pandas as pd
import os

def load_and_preprocess(data_dir: str) -> pd.DataFrame:
    dfs = []
    google_path = os.path.join(data_dir, 'google_ads_campaign_stats.csv')
    meta_path = os.path.join(data_dir, 'meta_ads_campaign_stats.csv')
    bing_path = os.path.join(data_dir, 'bing_campaign_stats.csv')
    
    if os.path.exists(google_path):
        df_google = pd.read_csv(google_path)
        col_mapping = {'Day': 'Date', 'Cost': 'Spend', 'Conv. value': 'Revenue', 'Conversion value': 'Revenue', 'Campaign type': 'CampaignType'}
        df_google = df_google.rename(columns=lambda x: col_mapping.get(x, x))
        df_google['Channel'] = 'Google'
        dfs.append(df_google)
        
    if os.path.exists(meta_path):
        df_meta = pd.read_csv(meta_path)
        col_mapping = {'Campaign name': 'Campaign', 'Amount spent (USD)': 'Spend', 'Amount spent': 'Spend', 'Link clicks': 'Clicks', 'Purchases': 'Conversions', 'Purchase conversion value': 'Revenue'}
        df_meta = df_meta.rename(columns=lambda x: col_mapping.get(x, x))
        df_meta['Channel'] = 'Meta'
        dfs.append(df_meta)
        
    if os.path.exists(bing_path):
        df_bing = pd.read_csv(bing_path)
        col_mapping = {'Gregorian date': 'Date', 'Time': 'Date', 'Campaign name': 'Campaign'}
        df_bing = df_bing.rename(columns=lambda x: col_mapping.get(x, x))
        df_bing['Channel'] = 'Bing'
        dfs.append(df_bing)
        
    if not dfs:
        raise FileNotFoundError("No valid dataset CSVs found in the data directory.")
        
    unified_df = pd.concat(dfs, ignore_index=True)
    
    # Ensure columns exist
    required = ['Date', 'Channel', 'Campaign', 'Spend', 'Clicks', 'Impressions', 'Conversions', 'Revenue']
    for col in required:
        if col not in unified_df.columns:
            unified_df[col] = 0
            
    unified_df['Date'] = pd.to_datetime(unified_df['Date'], errors='coerce')
    unified_df = unified_df.dropna(subset=['Date'])
    
    numeric_cols = ['Spend', 'Clicks', 'Impressions', 'Conversions', 'Revenue']
    for col in numeric_cols:
        unified_df[col] = pd.to_numeric(unified_df[col].replace('[\$,]', '', regex=True), errors='coerce').fillna(0)
        
    return unified_df
