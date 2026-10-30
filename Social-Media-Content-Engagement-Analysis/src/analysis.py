import pandas as pd
import numpy as np

def add_engagement_metrics(df):
    df = df.copy()
    cols = ['impressions', 'reach', 'likes', 'comments', 'shares']
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    df['total_engagements'] = df[['likes', 'comments', 'shares']].sum(axis=1)
    df['engagement_rate'] = np.where(df['reach'] > 0, df['total_engagements'] / df['reach'] * 100, 0)
    return df
