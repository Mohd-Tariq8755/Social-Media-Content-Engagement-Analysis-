# 🧪 Content Experiments Playbook: Social Media Testing Framework
**Project Code**: DA-020 Digital Marketing  
**Target Function**: Content Strategy, Creative Production, Social Media Management  

---

## Overview & Scientific Methodology

To translate analytical insights into verifiable marketing performance gains, the content team must run structured, controlled experiments rather than subjective design overhauls. 

Every experiment follows the standard **Hypothesis $\rightarrow$ Control vs. Variant $\rightarrow$ Statistical Power $\rightarrow$ Primary KPI $\rightarrow$ Decision Rule** protocol.

---

## Experiment 1: The Carousel Depth & Save CTA Test

### Background & Context
Our historical analysis proved that Carousels generate the highest Engagement Rate by Reach (13.11% ERR), propelled by a 3.34% Save Rate. However, production effort scales with carousel length (slides). We need to determine if longer carousels justify the creative production cost.

| Parameter | Specification |
| :--- | :--- |
| **Hypothesis** | Extending educational carousels from 4 slides to 8 slides with an explicit "Save for Later" prompt on the final card will increase the **Save Rate by at least +25%** without degrading swipe completion. |
| **Control Group (A)** | 12 Educational posts: 4-slide carousels with standard caption CTA. |
| **Variant Group (B)** | 12 Educational posts: 8-slide deep-dive carousels with dedicated "Save This Blueprint" end card. |
| **Controlled Variables** | Same topic category (Educational/How-To), published on Wednesdays at 10:00 AM, identical brand color palette. |
| **Primary Metric (KPI)** | **Save Rate ($VR\% = \frac{\text{Saves}}{\text{Reach}} \times 100$)** |
| **Secondary Metric** | Overall ERR % and Total Saves Count |
| **Sample Size & Duration** | 24 total posts over 8 weeks (3 posts/week) |
| **Success Threshold** | Variant B achieves $p < 0.05$ with minimum +20% relative lift in Save Rate. |
| **Decision Rule** | If successful, make 8-slide educational formats the standard operating procedure for all cornerstone guides. |

---

## Experiment 2: Mid-Week Prime Window Reallocation

### Background & Context
Historical data reveals that posts published on Wednesdays and Thursdays between 09:00 AM and 13:00 PM generate +34% higher interaction rates than weekend posts. Yet 25% of current post scheduling occurs on Saturday and Sunday.

| Parameter | Specification |
| :--- | :--- |
| **Hypothesis** | Reallocating 2 weekly weekend posts into Wednesday 10:00 AM and Thursday 12:30 PM slots will yield a **+20% increase in average Reach** and a **+30% lift in total weekly interactions**. |
| **Control Group (A)** | Status quo publishing schedule: 2 posts on Mon/Wed/Fri, 2 posts on Sat/Sun. |
| **Variant Group (B)** | Reallocated schedule: 0 weekend posts; 2 posts on Tuesday, 2 on Wednesday, 2 on Thursday, 1 on Friday afternoon. |
| **Controlled Variables** | Same format balance (40% Carousel, 30% Reel, 20% Infographic, 10% Poll) and total weekly volume (7 posts/week). |
| **Primary Metric (KPI)** | **Mean Post Reach** and **Weekly Total Interactions** |
| **Duration** | 6-week A/B time-series crossover test |
| **Success Threshold** | Variant schedule delivers $\ge 15\%$ higher average reach across identical content tiers. |
| **Decision Rule** | Cease standard weekend publishing and reassign editorial shifts to Monday-Thursday scheduling. |

---

## Experiment 3: Format Pivot: Static Image vs. 2-Card Infographic

### Background & Context
Static single images underperform dramatically (5.85% Mean ERR and 0.71% Share Rate). We want to test whether converting static graphics into 2-card modular infographics drives immediate amplification gains.

| Parameter | Specification |
| :--- | :--- |
| **Hypothesis** | Presenting industry statistics as a 2-card comparative infographic instead of a single static image will increase **Share Rate by $\ge +100\%$** (from ~0.7% to $\ge 1.5\%$). |
| **Control Group (A)** | 10 Industry Insight posts formatted as single static square graphics (1080x1080). |
| **Variant Group (B)** | 10 Industry Insight posts formatted as 2-card carousel infographics (Card 1: Problem Graphic, Card 2: Solution/Data Breakdown). |
| **Controlled Variables** | Matching data sources, identical headlines, published on Tuesdays at 11:00 AM. |
| **Primary Metric (KPI)** | **Share Rate ($SR\% = \frac{\text{Shares}}{\text{Reach}} \times 100$)** |
| **Secondary Metric** | Comment Rate and ERR % |
| **Sample Size & Duration** | 20 total posts over 5 weeks |
| **Decision Rule** | Completely retire static single images across the marketing department if Variant B achieves $> +50\%$ relative share lift. |

---

## Experiment Tracking Dashboard Template

| Experiment ID | Test Name | Start Date | End Date | Status | Control Value | Variant Value | % Lift | Statistical Sig. | Recommendation |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **EXP-001** | Carousel Depth (4 vs 8 slides) | 2024-07-01 | 2024-08-25 | Queued | 3.34% Saves | TBD | TBD | TBD | Pending |
| **EXP-002** | Mid-Week Window Reallocation | 2024-07-01 | 2024-08-11 | Queued | 8,500 Reach | TBD | TBD | TBD | Pending |
| **EXP-003** | Static Image to Infographic Pivot| 2024-07-15 | 2024-08-18 | Queued | 0.71% Shares | TBD | TBD | TBD | Pending |

