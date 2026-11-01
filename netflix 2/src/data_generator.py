"""
data_generator.py
Synthesizes a realistic social media marketing dataset (600 posts over 6 months).
Includes post metadata, delivery metrics (impressions, reach), interaction metrics
(likes, comments, shares, saves, clicks), and realistic edge cases (missing values).
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_social_media_data(num_posts: int = 600, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate realistic post-level social media dataset with intentional
    statistical nuances matching real-world digital marketing dynamics.
    """
    np.random.seed(random_seed)
    random.seed(random_seed)

    start_date = datetime(2024, 1, 1, 8, 0, 0)
    end_date = datetime(2024, 6, 30, 22, 0, 0)
    total_seconds = int((end_date - start_date).total_seconds())

    post_types = ['Carousel', 'Reel / Video', 'Static Image', 'Infographic', 'Text / Poll']
    type_weights = [0.30, 0.28, 0.22, 0.12, 0.08]

    content_categories = [
        'Educational / How-To',
        'Product Feature & Demo',
        'Industry Insights & Trends',
        'Behind The Scenes',
        'Community Spotlight / UGC',
        'Thought Leadership'
    ]
    category_weights = [0.28, 0.20, 0.18, 0.12, 0.12, 0.10]

    campaigns = [
        'Organic Evergreen',
        'Product_Launch_Q1',
        'Spring_Growth_Campaign',
        'Webinar_Promo',
        'Summer_Feature_Drop'
    ]
    campaign_weights = [0.45, 0.20, 0.15, 0.10, 0.10]

    # Hour weighting reflecting digital habits (morning, lunch, evening peaks)
    hour_weights = {
        6: 0.02, 7: 0.04, 8: 0.08, 9: 0.10, 10: 0.07,
        11: 0.05, 12: 0.09, 13: 0.09, 14: 0.06, 15: 0.04,
        16: 0.04, 17: 0.06, 18: 0.09, 19: 0.10, 20: 0.05, 21: 0.02
    }
    hours_list = list(hour_weights.keys())
    hours_prob = list(hour_weights.values())
    hours_prob = np.array(hours_prob) / sum(hours_prob)

    records = []

    # Generate dates across the 6-month span
    day_steps = sorted([random.randint(0, total_seconds) for _ in range(num_posts)])

    for i in range(num_posts):
        post_id = f"POST_{1000 + i + 1}"
        raw_dt = start_date + timedelta(seconds=day_steps[i])
        chosen_hour = np.random.choice(hours_list, p=hours_prob)
        minute = random.randint(0, 59)
        post_dt = raw_dt.replace(hour=int(chosen_hour), minute=minute, second=0)

        post_type = np.random.choice(post_types, p=type_weights)
        category = np.random.choice(content_categories, p=category_weights)
        campaign = np.random.choice(campaigns, p=campaign_weights)

        # Baseline delivery metrics dependent on format
        if post_type == 'Reel / Video':
            base_reach = int(np.random.lognormal(mean=9.8, sigma=0.6))  # mean ~22,000
            reach_to_imp_ratio = np.random.uniform(1.35, 2.4)
            like_rate = np.random.uniform(0.035, 0.065)
            comment_rate = np.random.uniform(0.003, 0.009)
            share_rate = np.random.uniform(0.008, 0.022)
            save_rate = np.random.uniform(0.006, 0.016)
        elif post_type == 'Carousel':
            base_reach = int(np.random.lognormal(mean=9.4, sigma=0.45)) # mean ~14,000
            reach_to_imp_ratio = np.random.uniform(1.2, 1.7)
            like_rate = np.random.uniform(0.045, 0.075)
            comment_rate = np.random.uniform(0.006, 0.015)
            share_rate = np.random.uniform(0.010, 0.026)
            save_rate = np.random.uniform(0.018, 0.042)  # Highest saves
        elif post_type == 'Infographic':
            base_reach = int(np.random.lognormal(mean=9.2, sigma=0.4))  # mean ~11,500
            reach_to_imp_ratio = np.random.uniform(1.15, 1.5)
            like_rate = np.random.uniform(0.040, 0.065)
            comment_rate = np.random.uniform(0.004, 0.010)
            share_rate = np.random.uniform(0.018, 0.038)  # Highest shares
            save_rate = np.random.uniform(0.015, 0.035)
        elif post_type == 'Static Image':
            base_reach = int(np.random.lognormal(mean=9.0, sigma=0.4))  # mean ~9,000
            reach_to_imp_ratio = np.random.uniform(1.1, 1.4)
            like_rate = np.random.uniform(0.028, 0.050)
            comment_rate = np.random.uniform(0.002, 0.006)
            share_rate = np.random.uniform(0.003, 0.009)
            save_rate = np.random.uniform(0.003, 0.008)
        else:  # Text / Poll
            base_reach = int(np.random.lognormal(mean=8.7, sigma=0.35)) # mean ~6,500
            reach_to_imp_ratio = np.random.uniform(1.05, 1.25)
            like_rate = np.random.uniform(0.022, 0.042)
            comment_rate = np.random.uniform(0.012, 0.030) # High comments
            share_rate = np.random.uniform(0.002, 0.007)
            save_rate = np.random.uniform(0.002, 0.006)

        # Category multipliers
        if category == 'Educational / How-To':
            save_rate *= 1.45
            share_rate *= 1.30
        elif category == 'Industry Insights & Trends':
            share_rate *= 1.40
            comment_rate *= 1.25
        elif category == 'Thought Leadership':
            comment_rate *= 1.50
            like_rate *= 1.15
        elif category == 'Behind The Scenes':
            like_rate *= 1.25
            save_rate *= 0.65

        # Day of week adjustments (Mid-week lift)
        dow = post_dt.weekday() # 0 = Monday, 6 = Sunday
        if dow in [2, 3]: # Wed, Thu
            reach_mult = 1.15
            eng_mult = 1.18
        elif dow in [5]: # Saturday
            reach_mult = 0.85
            eng_mult = 0.88
        elif dow in [6]: # Sunday evening save boost
            reach_mult = 0.95
            eng_mult = 1.05
            save_rate *= 1.25
        else:
            reach_mult = 1.0
            eng_mult = 1.0

        reach = int(max(500, base_reach * reach_mult))
        impressions = int(reach * reach_to_imp_ratio)

        # Engagement counts
        likes = int(reach * like_rate * eng_mult)
        comments = int(reach * comment_rate * eng_mult)
        shares = int(reach * share_rate * eng_mult)
        saves = int(reach * save_rate * eng_mult)

        # Profile/Link clicks
        click_rate = np.random.uniform(0.004, 0.018)
        clicks = int(reach * click_rate)

        # Caption length & hashtags
        caption_words = int(np.random.normal(loc=95, scale=40))
        caption_words = max(15, min(320, caption_words))
        hashtag_count = int(np.random.choice([0, 2, 3, 5, 7, 10, 12], p=[0.05, 0.15, 0.30, 0.25, 0.15, 0.08, 0.02]))

        # Media count
        if post_type == 'Carousel':
            media_count = random.randint(3, 10)
        elif post_type == 'Reel / Video':
            media_count = 1
        elif post_type == 'Infographic':
            media_count = random.randint(1, 3)
        else:
            media_count = 1

        record = {
            'post_id': post_id,
            'published_at': post_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'platform': 'Instagram',
            'post_type': post_type,
            'content_category': category,
            'campaign_tag': campaign,
            'media_count': media_count,
            'caption_length_words': caption_words,
            'hashtag_count': hashtag_count,
            'impressions': impressions,
            'reach': reach,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'saves': saves,
            'clicks': clicks
        }
        records.append(record)

    df = pd.DataFrame(records)

    # Introduce realistic missing values (simulating real platform API/export gaps)
    # 1. Reach missing in 3.5% of older records (simulating early legacy ingestion)
    missing_reach_indices = np.random.choice(df.index[:250], size=int(0.035 * len(df)), replace=False)
    df.loc[missing_reach_indices, 'reach'] = np.nan

    # 2. Shares missing in 2.5% of records (simulating private reshare tracking limitations)
    missing_share_indices = np.random.choice(df.index, size=int(0.025 * len(df)), replace=False)
    df.loc[missing_share_indices, 'shares'] = np.nan

    # 3. Saves missing in 2.0% of records
    missing_save_indices = np.random.choice(df.index, size=int(0.020 * len(df)), replace=False)
    df.loc[missing_save_indices, 'saves'] = np.nan

    return df

def save_datasets(df: pd.DataFrame, output_dir: str = 'data'):
    """
    Save generated dataset to CSV and styled multi-sheet Excel file.
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'social_media_engagement_data.csv')
    xlsx_path = os.path.join(output_dir, 'social_media_engagement_data.xlsx')

    df.to_csv(csv_path, index=False)
    print(f"Saved CSV dataset to: {csv_path} ({len(df)} rows)")

    # Data Dictionary definitions
    data_dict = [
        {'Column': 'post_id', 'Type': 'String', 'Description': 'Unique identifier for each published post (e.g., POST_1001)'},
        {'Column': 'published_at', 'Type': 'Datetime', 'Description': 'Timestamp when the post went live (YYYY-MM-DD HH:MM:SS)'},
        {'Column': 'platform', 'Type': 'String', 'Description': 'Social platform channel (Primary: Instagram)'},
        {'Column': 'post_type', 'Type': 'Categorical', 'Description': 'Media format: Carousel, Reel / Video, Static Image, Infographic, Text / Poll'},
        {'Column': 'content_category', 'Type': 'Categorical', 'Description': 'Strategic pillar: Educational, Product Feature, Industry Insights, Behind The Scenes, UGC, Thought Leadership'},
        {'Column': 'campaign_tag', 'Type': 'String', 'Description': 'Associated marketing campaign or evergreen label'},
        {'Column': 'media_count', 'Type': 'Integer', 'Description': 'Number of slides or media cards attached to post'},
        {'Column': 'caption_length_words', 'Type': 'Integer', 'Description': 'Word count of the post copy/caption'},
        {'Column': 'hashtag_count', 'Type': 'Integer', 'Description': 'Count of hashtags included in caption/first comment'},
        {'Column': 'impressions', 'Type': 'Integer', 'Description': 'Total count of times the post was displayed on screen (includes multiple views per user)'},
        {'Column': 'reach', 'Type': 'Float/Integer', 'Description': 'Count of unique accounts that saw the post at least once (Contains intentional missing values to reflect real exports)'},
        {'Column': 'likes', 'Type': 'Integer', 'Description': 'Total public like/heart reactions'},
        {'Column': 'comments', 'Type': 'Integer', 'Description': 'Total user replies and comments on the post'},
        {'Column': 'shares', 'Type': 'Float/Integer', 'Description': 'Direct message and external shares (Contains intentional nulls for privacy thresholds)'},
        {'Column': 'saves', 'Type': 'Float/Integer', 'Description': 'Post bookmarks/saves to collections (High indicator of intent/value)'},
        {'Column': 'clicks', 'Type': 'Integer', 'Description': 'Link clicks, sticker clicks, or profile destination taps'}
    ]
    df_dict = pd.DataFrame(data_dict)

    with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Raw_Post_Data', index=False)
        df_dict.to_excel(writer, sheet_name='Data_Dictionary', index=False)

    print(f"Saved Excel dataset to: {xlsx_path} with sheets: Raw_Post_Data, Data_Dictionary")
    return csv_path, xlsx_path

if __name__ == '__main__':
    data = generate_social_media_data(num_posts=600, random_seed=42)
    save_datasets(data)

