import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(by=['Channel', 'Date'])
    
    df['ROAS'] = np.where(df['Spend'] > 0, df['Revenue'] / df['Spend'], 0)
    df['CTR'] = np.where(df['Impressions'] > 0, df['Clicks'] / df['Impressions'], 0)
    df['ConversionRate'] = np.where(df['Clicks'] > 0, df['Conversions'] / df['Clicks'], 0)
    
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['Month'] = df['Date'].dt.month
    
    for window in [7, 30]:
        df[f'Revenue_Rolling_{window}'] = df.groupby('Channel')['Revenue'].transform(lambda x: x.rolling(window, min_periods=1).mean())
        df[f'Spend_Rolling_{window}'] = df.groupby('Channel')['Spend'].transform(lambda x: x.rolling(window, min_periods=1).mean())
        
    df = df.fillna(0)
    return df
