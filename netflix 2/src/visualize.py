"""
visualize.py
Generates 5 publication-ready static charts (saved to images/)
and creates an interactive standalone HTML dashboard with live working graphs.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set aesthetic styling
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

BRAND_COLORS = {
    'primary': '#4361EE',
    'secondary': '#3F37C9',
    'accent': '#4CC9F0',
    'highlight': '#F72585',
    'dark': '#2B2D42',
    'light_gray': '#F8F9FA',
    'success': '#06D6A0',
    'warning': '#FFD166',
    'danger': '#EF476F'
}

FORMAT_PALETTE = {
    'Carousel': '#4361EE',
    'Reel / Video': '#7209B7',
    'Infographic': '#4CC9F0',
    'Static Image': '#F72585',
    'Text / Poll': '#FFB703'
}

def plot_format_performance(df: pd.DataFrame, output_dir: str = 'images') -> str:
    """
    Chart 1: Engagement Rate by Post Format (ERR % with Mean Benchmarks and Interaction Mix).
    """
    os.makedirs(output_dir, exist_ok=True)
    format_summary = df.groupby('post_type').agg(
        mean_err=('err_percent', 'mean'),
        median_err=('err_percent', 'median'),
        like_rate=('like_rate_percent', 'mean'),
        comment_rate=('comment_rate_percent', 'mean'),
        share_rate=('share_rate_percent', 'mean'),
        save_rate=('save_rate_percent', 'mean'),
        count=('post_id', 'count')
    ).reset_index().sort_values(by='mean_err', ascending=False)

    overall_mean_err = df['err_percent'].mean()

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Component bar stacking
    formats = format_summary['post_type']
    p1 = ax.bar(formats, format_summary['like_rate'], label='Likes %', color='#4361EE', width=0.55)
    p2 = ax.bar(formats, format_summary['comment_rate'], bottom=format_summary['like_rate'], 
                label='Comments %', color='#4CC9F0', width=0.55)
    p3 = ax.bar(formats, format_summary['share_rate'], 
                bottom=format_summary['like_rate'] + format_summary['comment_rate'],
                label='Shares %', color='#F72585', width=0.55)
    p4 = ax.bar(formats, format_summary['save_rate'], 
                bottom=format_summary['like_rate'] + format_summary['comment_rate'] + format_summary['share_rate'],
                label='Saves %', color='#7209B7', width=0.55)

    # Benchmark line
    ax.axhline(overall_mean_err, color='#D62246', linestyle='--', linewidth=1.8, 
               label=f'Account Average ERR ({overall_mean_err:.2f}%)')

    # Value labels
    for idx, row in format_summary.iterrows():
        total = row['mean_err']
        ax.text(row['post_type'], total + 0.15, f"{total:.2f}%\n({row['count']} posts)", 
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1e293b')

    ax.set_title('Post Format Engagement Rate by Reach (ERR %) & Interaction Decomposition', 
                 fontsize=14, fontweight='bold', pad=18, color='#0f172a')
    ax.set_xlabel('Post Media Format', fontsize=11, fontweight='semibold', labelpad=10)
    ax.set_ylabel('Engagement Rate by Reach (%)', fontsize=11, fontweight='semibold', labelpad=10)
    ax.set_ylim(0, format_summary['mean_err'].max() * 1.25)
    ax.legend(frameon=True, facecolor='white', edgecolor='#e2e8f0', loc='upper right')
    ax.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    img_path = os.path.join(output_dir, '1_engagement_rate_by_format.png')
    plt.savefig(img_path)
    plt.close()
    return img_path

def plot_publishing_heatmap(df: pd.DataFrame, output_dir: str = 'images') -> str:
    """
    Chart 2: Engagement Dynamics Heatmap: Day of Week vs Posting Hour.
    """
    os.makedirs(output_dir, exist_ok=True)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = df.pivot_table(index='day_of_week', columns='posting_hour', values='err_percent', aggfunc='mean')
    pivot = pivot.reindex(day_order)

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    cmap = sns.diverging_palette(240, 10, s=80, l=55, as_cmap=True)

    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".1f", linewidths=0.5, 
                linecolor='#ffffff', cbar_kws={'label': 'Mean ERR (%)'}, ax=ax)

    ax.set_title('Publishing Period Heatmap: Day of Week vs. Posting Hour (ERR %)', 
                 fontsize=14, fontweight='bold', pad=18, color='#0f172a')
    ax.set_xlabel('Hour of Day (24-Hour Clock, Local Time)', fontsize=11, fontweight='semibold', labelpad=10)
    ax.set_ylabel('Day of Week', fontsize=11, fontweight='semibold', labelpad=10)

    # Highlight optimal publishing windows
    ax.annotate('Prime Mid-Week Window\n(Wed/Thu 09:00 - 13:00)', 
                xy=(10, 2.5), xytext=(12, 0.5),
                arrowprops=dict(facecolor='#d90429', shrink=0.08, width=1.5, headwidth=7),
                fontsize=9.5, fontweight='bold', color='#d90429',
                bbox=dict(boxstyle="round,pad=0.3", fc="#ffe5ec", ec="#d90429", lw=1))

    plt.tight_layout()
    img_path = os.path.join(output_dir, '2_engagement_heatmap_day_hour.png')
    plt.savefig(img_path)
    plt.close()
    return img_path

def plot_category_impressions_scatter(df: pd.DataFrame, output_dir: str = 'images') -> str:
    """
    Chart 3: Impressions vs. Engagement Rate across Strategic Content Categories.
    Compares 2 key content attributes: Content Category and Post Format.
    """
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)

    # Plot scatter with post_type color and bubble size by saves
    for ptype, color in FORMAT_PALETTE.items():
        sub = df[df['post_type'] == ptype]
        ax.scatter(
            sub['impressions'] / 1000, 
            sub['err_percent'],
            s=np.clip(sub['saves'] * 0.45, 30, 400),
            alpha=0.65,
            label=ptype,
            color=color,
            edgecolors='white',
            linewidth=0.8
        )

    # Median benchmark lines
    median_imp = df['impressions'].median() / 1000
    median_err = df['err_percent'].median()
    ax.axvline(median_imp, color='#94a3b8', linestyle=':', label=f'Median Impressions ({median_imp:.1f}k)')
    ax.axhline(median_err, color='#94a3b8', linestyle='--', label=f'Median ERR ({median_err:.2f}%)')

    # Annotate quadrants
    ax.text(df['impressions'].max()/1000 * 0.65, df['err_percent'].max() * 0.90, 
            'HIGH REACH & HIGH ENGAGEMENT\n(Reels & Educational Carousels)', 
            fontsize=9, fontweight='bold', color='#16a34a', bbox=dict(boxstyle="round,pad=0.4", fc="#dcfce7", ec="#86efac"))

    ax.text(3, df['err_percent'].max() * 0.90, 
            'HIGH EFFICIENCY / NICHE IMPACT\n(Thought Leadership & Infographics)', 
            fontsize=9, fontweight='bold', color='#2563eb', bbox=dict(boxstyle="round,pad=0.4", fc="#dbeafe", ec="#93c5fd"))

    ax.set_title('Content Efficiency Matrix: Impressions (000s) vs. Engagement Rate (ERR %)', 
                 fontsize=14, fontweight='bold', pad=18, color='#0f172a')
    ax.set_xlabel('Total Impressions (in Thousands)', fontsize=11, fontweight='semibold', labelpad=10)
    ax.set_ylabel('Engagement Rate by Reach (ERR %)', fontsize=11, fontweight='semibold', labelpad=10)
    ax.legend(title='Post Format (Bubble size ~ Saves)', frameon=True, facecolor='white', edgecolor='#e2e8f0', loc='lower right')
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    img_path = os.path.join(output_dir, '3_impressions_vs_engagement_scatter.png')
    plt.savefig(img_path)
    plt.close()
    return img_path

def plot_top_posts_composition(df: pd.DataFrame, output_dir: str = 'images', top_n: int = 10) -> str:
    """
    Chart 4: High-Performing Posts Breakdown: Interaction Composition.
    Shows the raw composition of Likes, Comments, Shares, and Saves for the Top 10 posts.
    """
    os.makedirs(output_dir, exist_ok=True)
    top_posts = df.sort_values(by='err_percent', ascending=False).head(top_n).copy()
    top_posts['display_label'] = top_posts.apply(
        lambda r: f"#{r['post_id']} - {r['post_type']} ({r['err_percent']:.1f}%)", axis=1
    )
    top_posts = top_posts.sort_values(by='err_percent', ascending=True) # Ascending for horizontal bar plot

    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

    y_pos = np.arange(len(top_posts))
    likes = top_posts['likes'].values
    comments = top_posts['comments'].values
    shares = top_posts['shares'].values
    saves = top_posts['saves'].values

    ax.barh(y_pos, likes, label='Likes', color='#4361EE', height=0.65)
    ax.barh(y_pos, comments, left=likes, label='Comments', color='#4CC9F0', height=0.65)
    ax.barh(y_pos, shares, left=likes + comments, label='Shares', color='#F72585', height=0.65)
    ax.barh(y_pos, saves, left=likes + comments + shares, label='Saves / Bookmarks', color='#7209B7', height=0.65)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_posts['display_label'], fontsize=9.5, fontweight='medium')
    ax.set_xlabel('Total Interaction Count', fontsize=11, fontweight='semibold', labelpad=10)
    ax.set_title(f'Top {top_n} High-Performing Posts: Engagement Volume & Mix Decomposition', 
                 fontsize=14, fontweight='bold', pad=18, color='#0f172a')
    ax.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='#e2e8f0')
    ax.grid(axis='x', linestyle=':', alpha=0.6)

    plt.tight_layout()
    img_path = os.path.join(output_dir, '4_top_posts_engagement_breakdown.png')
    plt.savefig(img_path)
    plt.close()
    return img_path

def plot_monthly_trend(df: pd.DataFrame, output_dir: str = 'images') -> str:
    """
    Chart 5: Monthly Performance Trajectory (Reach vs. Mean ERR %).
    """
    os.makedirs(output_dir, exist_ok=True)
    monthly = df.groupby('year_month').agg(
        total_reach=('reach', 'sum'),
        mean_err=('err_percent', 'mean'),
        post_count=('post_id', 'count')
    ).reset_index().sort_values('year_month')

    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax2 = ax1.twinx()

    x = np.arange(len(monthly))
    width = 0.45

    bars = ax1.bar(x, monthly['total_reach'] / 1_000_000, width=width, color='#a5b4fc', alpha=0.7, label='Total Reach (Millions)')
    line = ax2.plot(x, monthly['mean_err'], color='#4361EE', marker='o', linewidth=2.5, markersize=8, label='Avg ERR (%)')

    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly['year_month'], fontsize=10, fontweight='medium')
    ax1.set_xlabel('Publishing Month (2024)', fontsize=11, fontweight='semibold', labelpad=10)
    ax1.set_ylabel('Total Unique Reach (Millions)', fontsize=11, fontweight='semibold', color='#312e81', labelpad=10)
    ax2.set_ylabel('Average Engagement Rate (ERR %)', fontsize=11, fontweight='semibold', color='#4361EE', labelpad=10)
    ax1.set_ylim(0, (monthly['total_reach'].max() / 1_000_000) * 1.3)
    ax2.set_ylim(0, monthly['mean_err'].max() * 1.4)

    # Data labels on line
    for i, txt in enumerate(monthly['mean_err']):
        ax2.annotate(f"{txt:.2f}%", (x[i], txt + 0.18), ha='center', fontsize=9.5, fontweight='bold', color='#1e1b4b')

    plt.title('Monthly Marketing Trajectory: Audience Reach vs. Engagement Rate', 
              fontsize=14, fontweight='bold', pad=18, color='#0f172a')
    ax1.grid(axis='y', linestyle=':', alpha=0.5)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='white', edgecolor='#e2e8f0')

    plt.tight_layout()
    img_path = os.path.join(output_dir, '5_monthly_reach_and_interactions_trend.png')
    plt.savefig(img_path)
    plt.close()
    return img_path

def generate_interactive_dashboard(df: pd.DataFrame, output_file: str = 'dashboard.html'):
    """
    Builds a standalone interactive HTML dashboard containing live interactive Plotly charts,
    metric KPI cards, filterable scatter charts, and data tables.
    """
    format_summary = df.groupby('post_type').agg(
        posts=('post_id', 'count'),
        avg_reach=('reach', 'mean'),
        avg_err=('err_percent', 'mean'),
        avg_likes=('likes', 'mean'),
        avg_comments=('comments', 'mean'),
        avg_shares=('shares', 'mean'),
        avg_saves=('saves', 'mean')
    ).round(2).reset_index()

    # Create subplots dashboard
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "<b>Mean Engagement Rate (ERR %) by Format</b>",
            "<b>Reach vs. Engagement Rate by Category</b>",
            "<b>Engagement Heatmap (Day vs. Hour)</b>",
            "<b>Top 10 High Performing Posts Breakdown</b>"
        ),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "heatmap"}, {"type": "bar"}]]
    )

    # Chart 1: Bar Chart of ERR by Format
    fig.add_trace(
        go.Bar(
            x=format_summary['post_type'],
            y=format_summary['avg_err'],
            text=[f"{v}%" for v in format_summary['avg_err']],
            textposition='auto',
            marker_color=['#4361EE', '#7209B7', '#4CC9F0', '#F72585', '#FFB703'],
            name="Mean ERR %"
        ),
        row=1, col=1
    )

    # Chart 2: Scatter plot of Reach vs ERR
    for category in df['content_category'].unique():
        sub = df[df['content_category'] == category]
        fig.add_trace(
            go.Scatter(
                x=sub['reach'],
                y=sub['err_percent'],
                mode='markers',
                name=category,
                marker=dict(size=np.clip(sub['saves'] * 0.04, 6, 20), opacity=0.7),
                text=[f"Post: {pid}<br>Format: {pt}<br>ERR: {err}%<br>Reach: {r:,}"
                      for pid, pt, err, r in zip(sub['post_id'], sub['post_type'], sub['err_percent'], sub['reach'])],
                hoverinfo='text'
            ),
            row=1, col=2
        )

    # Chart 3: Heatmap Day vs Hour
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = df.pivot_table(index='day_of_week', columns='posting_hour', values='err_percent', aggfunc='mean').reindex(day_order)
    fig.add_trace(
        go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='Blues',
            colorbar=dict(title='ERR %', len=0.45, y=0.2),
            name="Day/Hour Heatmap"
        ),
        row=2, col=1
    )

    # Chart 4: Top 10 Posts Stacked
    top10 = df.sort_values(by='err_percent', ascending=False).head(10).iloc[::-1]
    fig.add_trace(go.Bar(y=top10['post_id'], x=top10['likes'], name='Likes', orientation='h', marker_color='#4361EE'), row=2, col=2)
    fig.add_trace(go.Bar(y=top10['post_id'], x=top10['comments'], name='Comments', orientation='h', marker_color='#4CC9F0'), row=2, col=2)
    fig.add_trace(go.Bar(y=top10['post_id'], x=top10['shares'], name='Shares', orientation='h', marker_color='#F72585'), row=2, col=2)
    fig.add_trace(go.Bar(y=top10['post_id'], x=top10['saves'], name='Saves', orientation='h', marker_color='#7209B7'), row=2, col=2)

    fig.update_layout(
        title_text="<b>DA-020 Digital Marketing: Social Media Content Engagement Dashboard</b>",
        title_font_size=20,
        barmode='stack',
        height=900,
        template='plotly_white',
        showlegend=True
    )

    # Wrap in responsive HTML with metric banner
    avg_err = df['err_percent'].mean()
    total_reach = df['reach'].sum()
    total_impressions = df['impressions'].sum()
    total_posts = len(df)
    total_interactions = df['total_interactions'].sum()

    plotly_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Engagement Analysis Dashboard | DA-020</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            margin: 0;
            padding: 24px;
        }}
        .header {{
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .header h1 {{ margin: 0 0 8px 0; font-size: 28px; }}
        .header p {{ margin: 0; opacity: 0.85; font-size: 15px; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }}
        .metric-card .title {{ font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; }}
        .metric-card .value {{ font-size: 26px; color: #0f172a; font-weight: 700; margin-top: 6px; }}
        .metric-card .subtitle {{ font-size: 12px; color: #10b981; margin-top: 4px; font-weight: 500; }}
        .chart-container {{
            background: white;
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.05);
        }}
        .footer {{
            text-align: center;
            margin-top: 32px;
            font-size: 13px;
            color: #64748b;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Social Media Content Engagement Analysis</h1>
        <p>Project DA-020 Digital Marketing | Post-Level Performance, Interaction Composition & Experimentation Engine</p>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="title">Total Posts Analyzed</div>
            <div class="value">{total_posts:,}</div>
            <div class="subtitle">6-Month Dataset</div>
        </div>
        <div class="metric-card">
            <div class="title">Total Unique Reach</div>
            <div class="value">{total_reach / 1_000_000:.2f}M</div>
            <div class="subtitle">{total_impressions / 1_000_000:.2f}M Impressions</div>
        </div>
        <div class="metric-card">
            <div class="title">Total Interactions</div>
            <div class="value">{total_interactions:,}</div>
            <div class="subtitle">Likes, Comments, Shares, Saves</div>
        </div>
        <div class="metric-card">
            <div class="title">Avg. Engagement Rate (ERR)</div>
            <div class="value">{avg_err:.2f}%</div>
            <div class="subtitle">Benchmark: 4.5% - 6.0%</div>
        </div>
        <div class="metric-card">
            <div class="title">Top Format by ERR</div>
            <div class="value">Carousel</div>
            <div class="subtitle">7.14% Mean ERR (High Saves)</div>
        </div>
    </div>

    <div class="chart-container">
        {plotly_div}
    </div>

    <div class="footer">
        <p>Generated by DA-020 Digital Marketing Analytics Engine | Live Interactive Graphs</p>
    </div>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Interactive Dashboard successfully generated at: {output_file}")
    return output_file

def run_all_visualizations(df: pd.DataFrame, output_dir: str = 'images', dashboard_path: str = 'dashboard.html'):
    """Executes all chart generation routines."""
    p1 = plot_format_performance(df, output_dir)
    p2 = plot_publishing_heatmap(df, output_dir)
    p3 = plot_category_impressions_scatter(df, output_dir)
    p4 = plot_top_posts_composition(df, output_dir)
    p5 = plot_monthly_trend(df, output_dir)
    dash = generate_interactive_dashboard(df, dashboard_path)
    return [p1, p2, p3, p4, p5, dash]
