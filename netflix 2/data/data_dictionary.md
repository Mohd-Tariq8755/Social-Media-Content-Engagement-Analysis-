# 📖 Data Dictionary & Metric Governance (DA-020)

This document provides definitive metric definitions, underlying calculation formulas, denominator specifications, and data handling policies for the post-level social media dataset.

---

## 1. Raw Dataset Columns & Attributes

| Column Name | Data Type | Nullable? | Description & Value Range | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `post_id` | String | No | Unique post identifier | `POST_1001` |
| `published_at` | Datetime | No | ISO-8601 timestamp of publication | `2024-03-14 10:15:00` |
| `platform` | String | No | Social media channel | `Instagram` |
| `post_type` | Categorical | No | Format: `Carousel`, `Reel / Video`, `Static Image`, `Infographic`, `Text / Poll` | `Carousel` |
| `content_category` | Categorical | No | Strategic theme: `Educational / How-To`, `Product Feature & Demo`, `Industry Insights & Trends`, `Behind The Scenes`, `Community Spotlight / UGC`, `Thought Leadership` | `Educational / How-To` |
| `campaign_tag` | String | No | Associated initiative (e.g., `Organic Evergreen`, `Product_Launch_Q1`) | `Organic Evergreen` |
| `media_count` | Integer | No | Count of images, video clips, or carousel slides (1 to 10) | `6` |
| `caption_length_words`| Integer | No | Total word count of post copy | `124` |
| `hashtag_count` | Integer | No | Count of hashtags placed in caption | `5` |
| `impressions` | Integer | No | Gross number of times post appeared on user screens | `24,500` |
| `reach` | Float | **Yes (3.5%)** | Unique user accounts that viewed the post | `16,200` |
| `likes` | Integer | No | Public heart / reaction count | `820` |
| `comments` | Integer | No | Public comment and conversational reply count | `74` |
| `shares` | Float | **Yes (2.5%)** | Direct message shares, external forwards, and story reposts | `142` |
| `saves` | Float | **Yes (2.0%)** | Bookmarks saved to private collections | `310` |
| `clicks` | Integer | No | Profile visits, link-in-bio clicks, or sticker taps | `185` |

---

## 2. Calculated Metrics & Formal Definitions

### 2.1 Engagement Rate by Reach (ERR %) — Primary Metric
$$\text{ERR} (\%) = \left( \frac{\text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}}{\text{Reach}} \right) \times 100$$
* **Denominator**: `reach` (Unique accounts exposed).
* **Rationale**: Normalizes engagement against actual unique audience exposure, eliminating viral impression skew.

### 2.2 Engagement Rate by Impressions (ERI %) — Secondary Metric
$$\text{ERI} (\%) = \left( \frac{\text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}}{\text{Impressions}} \right) \times 100$$
* **Denominator**: `impressions` (Total displays).
* **Rationale**: Useful for cross-channel and paid media comparability where reach is often modeled.

### 2.3 Individual Interaction Rates (% of Reach)
* **Like Rate**: $\text{LR} (\%) = \frac{\text{Likes}}{\text{Reach}} \times 100$
* **Comment Rate**: $\text{CR} (\%) = \frac{\text{Comments}}{\text{Reach}} \times 100$
* **Share Rate (Amplification)**: $\text{SR} (\%) = \frac{\text{Shares}}{\text{Reach}} \times 100$
* **Save Rate (Virality / High Intent)**: $\text{VR} (\%) = \frac{\text{Saves}}{\text{Reach}} \times 100$
* **Click-Through Rate (CTR)**: $\text{CTR} (\%) = \frac{\text{Clicks}}{\text{Impressions}} \times 100$
* **Frequency**: $\text{Frequency} = \frac{\text{Impressions}}{\text{Reach}}$

---

## 3. Data Cleansing & Missing Value Policy

| Field | Nature of Missingness | Cleaning & Imputation Strategy |
| :--- | :--- | :--- |
| `reach` | Legacy ingestion latency / format sync differences | **Cohort Frequency Imputation**: Calculate median $\text{Frequency} = \frac{\text{Impressions}}{\text{Reach}}$ for each `post_type`. Impute missing reach as $\widehat{\text{Reach}} = \text{round}\left(\frac{\text{Impressions}}{\text{Format Median Frequency}}\right)$. |
| `shares` | Privacy restrictions on private DMs | **Conservative Zero-Fill**: Impute `NaN` $\rightarrow$ `0` after recording `shares_was_missing = True`. |
| `saves` | API version deprecation on older posts | **Conservative Zero-Fill**: Impute `NaN` $\rightarrow$ `0` after recording `saves_was_missing = True`. |

