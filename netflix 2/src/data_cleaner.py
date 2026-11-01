"""
data_cleaner.py
Handles missing values, data validation, metric calculations, and feature engineering
for social media post-level engagement analysis.
"""

import numpy as np
import pandas as pd

def clean_and_prepare_social_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw post data:
    1. Parse timestamps into publishing periods (date, day of week, hour, daypart).
    2. Document & handle missing metrics (impute missing reach using format frequency; fill null interactions with 0).
    3. Calculate documented engagement metrics and interaction rates.
    """
    df_clean = df.copy()

    # 1. Parse timestamps
    df_clean['published_at'] = pd.to_datetime(df_clean['published_at'])
    df_clean['publish_date'] = df_clean['published_at'].dt.date
    df_clean['year_month'] = df_clean['published_at'].dt.to_period('M').astype(str)
    df_clean['day_of_week'] = df_clean['published_at'].dt.day_name()
    df_clean['day_of_week_num'] = df_clean['published_at'].dt.dayofweek
    df_clean['is_weekend'] = df_clean['day_of_week_num'].apply(lambda x: 1 if x in [5, 6] else 0)
    df_clean['posting_hour'] = df_clean['published_at'].dt.hour

    def assign_daypart(hour):
        if 6 <= hour < 9:
            return 'Early Morning (06-09)'
        elif 9 <= hour < 12:
            return 'Morning Peak (09-12)'
        elif 12 <= hour < 15:
            return 'Midday / Lunch (12-15)'
        elif 15 <= hour < 18:
            return 'Afternoon (15-18)'
        elif 18 <= hour < 21:
            return 'Evening Peak (18-21)'
        else:
            return 'Night / Off-Hours (21-06)'

    df_clean['daypart_slot'] = df_clean['posting_hour'].apply(assign_daypart)

    # 2. Document and handle missing metrics
    # Track missingness indicators
    df_clean['reach_was_missing'] = df_clean['reach'].isna()
    df_clean['shares_was_missing'] = df_clean['shares'].isna()
    df_clean['saves_was_missing'] = df_clean['saves'].isna()

    # Strategy for missing interactions (shares, saves): replace NaN with 0 (conservative assumption)
    df_clean['shares'] = df_clean['shares'].fillna(0).astype(int)
    df_clean['saves'] = df_clean['saves'].fillna(0).astype(int)
    df_clean['likes'] = df_clean['likes'].fillna(0).astype(int)
    df_clean['comments'] = df_clean['comments'].fillna(0).astype(int)
    df_clean['clicks'] = df_clean['clicks'].fillna(0).astype(int)

    # Strategy for missing reach:
    # Reach is the primary denominator for Engagement Rate (ERR).
    # Where reach is available, calculate format-specific Frequency = Impressions / Reach.
    # Where reach is missing, impute Reach = round(Impressions / format_median_frequency).
    complete_reach_mask = df_clean['reach'].notna() & (df_clean['reach'] > 0)
    format_freq = (df_clean.loc[complete_reach_mask, 'impressions'] / 
                   df_clean.loc[complete_reach_mask, 'reach']).groupby(df_clean['post_type']).median()

    # Fallback overall frequency if format has no data
    overall_median_freq = 1.35

    def impute_reach(row):
        if pd.isna(row['reach']) or row['reach'] == 0:
            freq = format_freq.get(row['post_type'], overall_median_freq)
            return int(round(row['impressions'] / freq))
        return int(row['reach'])

    df_clean['reach'] = df_clean.apply(impute_reach, axis=1)

    # Calculate actual post frequency
    df_clean['frequency'] = np.round(df_clean['impressions'] / df_clean['reach'], 2)

    # 3. Calculate documented metrics
    # Total Interactions = Likes + Comments + Shares + Saves
    df_clean['total_interactions'] = (
        df_clean['likes'] + df_clean['comments'] + df_clean['shares'] + df_clean['saves']
    )

    # Total Engagements (including clicks)
    df_clean['total_engagements'] = df_clean['total_interactions'] + df_clean['clicks']

    # Engagement Rate by Reach (ERR %) = (Total Interactions / Reach) * 100
    df_clean['err_percent'] = np.round((df_clean['total_interactions'] / df_clean['reach']) * 100, 2)

    # Engagement Rate by Impressions (ERI %) = (Total Interactions / Impressions) * 100
    df_clean['eri_percent'] = np.round((df_clean['total_interactions'] / df_clean['impressions']) * 100, 2)

    # Individual Interaction Rates (% of Reach)
    df_clean['like_rate_percent'] = np.round((df_clean['likes'] / df_clean['reach']) * 100, 2)
    df_clean['comment_rate_percent'] = np.round((df_clean['comments'] / df_clean['reach']) * 100, 2)
    df_clean['share_rate_percent'] = np.round((df_clean['shares'] / df_clean['reach']) * 100, 2)
    df_clean['save_rate_percent'] = np.round((df_clean['saves'] / df_clean['reach']) * 100, 2)
    df_clean['ctr_percent'] = np.round((df_clean['clicks'] / df_clean['impressions']) * 100, 2)

    # Performance tier based on ERR quartiles
    q25 = df_clean['err_percent'].quantile(0.25)
    q75 = df_clean['err_percent'].quantile(0.75)
    q90 = df_clean['err_percent'].quantile(0.90)

    def assign_tier(val):
        if val >= q90:
            return 'Top 10% Superstar'
        elif val >= q75:
            return 'High Performer'
        elif val >= q25:
            return 'Average Performer'
        else:
            return 'Underperforming'

    df_clean['performance_tier'] = df_clean['err_percent'].apply(assign_tier)

    return df_clean

if __name__ == '__main__':
    from data_generator import generate_social_media_data
    raw_df = generate_social_media_data(100)
    clean_df = clean_and_prepare_social_data(raw_df)
    print("Cleaned dataframe summary:")
    print(clean_df[['post_id', 'post_type', 'reach', 'err_percent', 'performance_tier']].head())

