"""
main.py
End-to-End Orchestrator for Social Media Content Engagement Analysis (DA-020).
Runs data generation, metric cleaning, statistical analysis, image generation,
and interactive dashboard deployment.
"""

import os
import sys

# Ensure UTF-8 output encoding on Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import pandas as pd
from src.data_generator import generate_social_media_data, save_datasets
from src.data_cleaner import clean_and_prepare_social_data
from src.analytics import (
    analyze_by_format,
    analyze_by_category,
    analyze_format_by_category,
    analyze_publishing_periods,
    get_performance_rankings,
    get_monthly_trends
)
from src.visualize import run_all_visualizations

def main():
    print("=" * 70)
    print("[PROJECT] DA-020: SOCIAL MEDIA CONTENT ENGAGEMENT ANALYSIS PIPELINE")
    print("=" * 70)

    # 1. Dataset Generation
    print("\n[Step 1/5] Synthesizing 6-Month Post-Level Dataset...")
    raw_df = generate_social_media_data(num_posts=600, random_seed=42)
    csv_path, xlsx_path = save_datasets(raw_df, output_dir='data')
    print(f"  -> Raw posts generated: {len(raw_df):,}")
    print(f"  -> Missing reach simulated: {raw_df['reach'].isna().sum()} posts")
    print(f"  -> Missing shares simulated: {raw_df['shares'].isna().sum()} posts")

    # 2. Data Cleaning & Metric Calculations
    print("\n[Step 2/5] Cleaning Data & Computing Documented Engagement Formulas...")
    clean_df = clean_and_prepare_social_data(raw_df)
    clean_csv_path = 'data/cleaned_social_media_engagement.csv'
    clean_df.to_csv(clean_csv_path, index=False)
    print(f"  -> Imputed missing values & calculated ERR%, ERI%, component rates.")
    print(f"  -> Cleaned dataset saved to: {clean_csv_path}")

    # 3. Statistical Analysis & Groupings
    print("\n[Step 3/5] Running Multi-Attribute Statistical Groupings...")
    format_summary = analyze_by_format(clean_df)
    category_summary = analyze_by_category(clean_df)
    cross_summary = analyze_format_by_category(clean_df)
    pub_periods = analyze_publishing_periods(clean_df)
    top_posts = get_performance_rankings(clean_df, top_n=10)
    monthly = get_monthly_trends(clean_df)

    print("\n--- POST FORMAT PERFORMANCE RANKING ---")
    print(format_summary[['post_type', 'post_count', 'avg_reach', 'mean_err_percent', 'save_rate_percent', 'share_rate_percent']].to_string(index=False))

    print("\n--- CONTENT CATEGORY PERFORMANCE ---")
    print(category_summary[['content_category', 'post_count', 'avg_reach', 'mean_err_percent', 'save_rate_percent']].to_string(index=False))

    print("\n--- TOP 5 PERFORMING POSTS ---")
    print(top_posts[['rank', 'post_id', 'post_type', 'content_category', 'reach', 'err_percent', 'saves']].head().to_string(index=False))

    # Save summary tables to data/
    with pd.ExcelWriter('data/analysis_summary_tables.xlsx', engine='openpyxl') as writer:
        format_summary.to_excel(writer, sheet_name='By_Format', index=False)
        category_summary.to_excel(writer, sheet_name='By_Category', index=False)
        cross_summary.to_excel(writer, sheet_name='Format_x_Category', index=False)
        pub_periods['dow_summary'].to_excel(writer, sheet_name='By_DayOfWeek', index=False)
        pub_periods['daypart_summary'].to_excel(writer, sheet_name='By_Daypart', index=False)
        top_posts.to_excel(writer, sheet_name='Top_10_Rankings', index=False)
        monthly.to_excel(writer, sheet_name='Monthly_Trajectory', index=False)
    print("  -> Exported detailed summary tables to: data/analysis_summary_tables.xlsx")

    # 4. Chart Generation (Images)
    print("\n[Step 4/5] Rendering 5 Publication-Ready Charts to images/ ...")
    generated_charts = run_all_visualizations(clean_df, output_dir='images', dashboard_path='dashboard.html')
    for chart in generated_charts[:5]:
        print(f"  -> Generated static chart: {chart}")

    # 5. Live Interactive Dashboard
    print(f"\n[Step 5/5] Deployed Live Working Graph Dashboard: {generated_charts[5]}")

    print("\n" + "=" * 70)
    print("[SUCCESS] ANALYSIS PIPELINE COMPLETE! All outputs, charts & dashboard are ready.")
    print("=" * 70)

if __name__ == '__main__':
    main()
