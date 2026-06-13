import pandas as pd
import numpy as np

def generate_mock_data():
    dates = pd.date_range(start='2025-01-01', periods=100, freq='D')
    
    # Google
    google_df = pd.DataFrame({
        'Date': dates,
        'Campaign': 'Google_Search_Brand',
        'Campaign type': 'Search',
        'Cost': np.random.uniform(100, 500, 100),
        'Clicks': np.random.randint(50, 200, 100),
        'Impressions': np.random.randint(1000, 5000, 100),
        'Conversions': np.random.randint(5, 50, 100)
    })
    google_df['Conv. value'] = google_df['Cost'] * np.random.uniform(2, 5, 100)
    google_df.to_csv('data/google_ads_campaign_stats.csv', index=False)
    
    # Meta
    meta_df = pd.DataFrame({
        'Date': dates,
        'Campaign name': 'Meta_Retargeting',
        'Amount spent (USD)': np.random.uniform(50, 300, 100),
        'Link clicks': np.random.randint(30, 150, 100),
        'Impressions': np.random.randint(2000, 8000, 100),
        'Purchases': np.random.randint(2, 30, 100)
    })
    meta_df['Purchase conversion value'] = meta_df['Amount spent (USD)'] * np.random.uniform(1.5, 4, 100)
    meta_df.to_csv('data/meta_ads_campaign_stats.csv', index=False)
    
    # Bing
    bing_df = pd.DataFrame({
        'Time': dates,
        'Campaign name': 'Bing_Generic',
        'Spend': np.random.uniform(20, 150, 100),
        'Clicks': np.random.randint(10, 80, 100),
        'Impressions': np.random.randint(500, 2000, 100),
        'Conversions': np.random.randint(1, 20, 100)
    })
    bing_df['Revenue'] = bing_df['Spend'] * np.random.uniform(3, 7, 100)
    bing_df.to_csv('data/bing_campaign_stats.csv', index=False)

if __name__ == "__main__":
    generate_mock_data()
