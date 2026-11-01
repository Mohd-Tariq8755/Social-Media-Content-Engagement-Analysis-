"""
analytics.py
Performs statistical grouping, comparative analysis across content attributes,
performance rankings, and generates actionable summary metrics for content planning.
"""

import numpy as np
import pandas as pd

def analyze_by_format(df: pd.DataFrame) -> pd.DataFrame:
    """Compare performance across post formats/types."""
    summary = df.groupby('post_type').agg(
        post_count=('post_id', 'count'),
        avg_reach=('reach', 'mean'),
        avg_impressions=('impressions', 'mean'),
        mean_err_percent=('err_percent', 'mean'),
        median_err_percent=('err_percent', 'median'),
        mean_eri_percent=('eri_percent', 'mean'),
        like_rate_percent=('like_rate_percent', 'mean'),
        comment_rate_percent=('comment_rate_percent', 'mean'),
        share_rate_percent=('share_rate_percent', 'mean'),
        save_rate_percent=('save_rate_percent', 'mean')
    ).reset_index()

    summary['post_share_pct'] = (summary['post_count'] / summary['post_count'].sum()) * 100
    summary = summary.sort_values(by='mean_err_percent', ascending=False).round(2)
    return summary

def analyze_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Compare performance across strategic content categories."""
    summary = df.groupby('content_category').agg(
        post_count=('post_id', 'count'),
        avg_reach=('reach', 'mean'),
        avg_impressions=('impressions', 'mean'),
        mean_err_percent=('err_percent', 'mean'),
        median_err_percent=('err_percent', 'median'),
        total_interactions=('total_interactions', 'sum'),
        save_rate_percent=('save_rate_percent', 'mean'),
        share_rate_percent=('share_rate_percent', 'mean')
    ).reset_index().sort_values(by='mean_err_percent', ascending=False).round(2)
    return summary

def analyze_format_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Two-attribute cross analysis: Post Type x Content Category."""
    cross = df.groupby(['post_type', 'content_category']).agg(
        post_count=('post_id', 'count'),
        avg_reach=('reach', 'mean'),
        mean_err_percent=('err_percent', 'mean'),
        save_rate_percent=('save_rate_percent', 'mean')
    ).reset_index().sort_values(by=['post_type', 'mean_err_percent'], ascending=[True, False]).round(2)
    return cross

def analyze_publishing_periods(df: pd.DataFrame) -> dict:
    """Analyze engagement dynamics by Day of Week and Posting Time Slot."""
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Day of week grouping
    dow_summary = df.groupby('day_of_week').agg(
        post_count=('post_id', 'count'),
        avg_reach=('reach', 'mean'),
        mean_err_percent=('err_percent', 'mean'),
        median_err_percent=('err_percent', 'median'),
        avg_total_interactions=('total_interactions', 'mean')
    ).reindex(day_order).reset_index().round(2)

    # Daypart grouping
    daypart_order = [
        'Early Morning (06-09)',
        'Morning Peak (09-12)',
        'Midday / Lunch (12-15)',
        'Afternoon (15-18)',
        'Evening Peak (18-21)',
        'Night / Off-Hours (21-06)'
    ]
    daypart_summary = df.groupby('daypart_slot').agg(
        post_count=('post_id', 'count'),
        avg_reach=('reach', 'mean'),
        mean_err_percent=('err_percent', 'mean'),
        median_err_percent=('err_percent', 'median')
    ).reindex(daypart_order).dropna(how='all').reset_index().round(2)

    # Pivot table for Day x Hour heatmap
    day_hour_pivot = df.pivot_table(
        index='day_of_week',
        columns='posting_hour',
        values='err_percent',
        aggfunc='mean'
    ).reindex(day_order)

    return {
        'dow_summary': dow_summary,
        'daypart_summary': daypart_summary,
        'day_hour_pivot': day_hour_pivot
    }

def get_performance_rankings(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Identify top-performing posts ranked by Engagement Rate by Reach (ERR %)."""
    top_posts = df.sort_values(by='err_percent', ascending=False).head(top_n).copy()
    top_posts['rank'] = range(1, top_n + 1)
    cols = [
        'rank', 'post_id', 'post_type', 'content_category', 'published_at',
        'reach', 'impressions', 'err_percent', 'likes', 'comments', 'shares', 'saves'
    ]
    return top_posts[cols]

def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly performance trajectory."""
    monthly = df.groupby('year_month').agg(
        posts_published=('post_id', 'count'),
        total_reach=('reach', 'sum'),
        total_impressions=('impressions', 'sum'),
        total_interactions=('total_interactions', 'sum'),
        avg_err_percent=('err_percent', 'mean')
    ).reset_index().sort_values(by='year_month').round(2)
    return monthly

