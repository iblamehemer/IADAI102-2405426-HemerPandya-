
# ⚽ Player Injuries & Team Performance Dashboard

## Overview

This project is part of the **Mathematics for AI – II (Artificial Intelligence)** course.

It analyses the relationship between **player injuries** and **team performance** over multiple seasons using Python and presents the insights through an interactive **Streamlit dashboard**.

The dashboard is designed for **technical directors, sports analysts, and coaches** to:

- Understand how injuries affect match outcomes and points.
- Identify which clubs suffer the most during injury periods.
- Track player performance before and after injuries.
- Detect injury clusters across months and clubs.
- Explore the relationship between player age and performance change.

---

## Scenario

**Scenario 1: Player Injuries and Team Performance Dashboard**

FootLens Analytics has acquired a dataset of player injuries and team performance.
As a Junior Sports Data Analyst, you must build an interactive dashboard that links injuries with team results and player ratings.

---

## Key Features

- 📊 **Team Performance Drop Index** during injury periods.
- 📈 **Player Performance Timeline** (rating before, during and after injury).
- 🔥 **Heatmap of Injury Frequency** across months and clubs.
- 🎯 **Age vs Rating Change Scatter Plot** (impact of age on comeback).
- 🏆 **Comeback Leaderboard**: players with the biggest post-injury improvement.
- 🧮 Filters by **team** and **player**.
- 🧾 Option to view **raw cleaned data**.

---

## Tech Stack

- **Python**
- **Pandas**, **NumPy**
- **Plotly Express**
- **Streamlit**

---

## Folder Structure

```text
.
├── app.py
├── injuries.csv              # your dataset (not included here)
├── requirements.txt
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your dataset (e.g., `injuries.csv`) into the project folder.

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## Deployment on Streamlit Cloud

1. Push this repository to GitHub.
2. Go to Streamlit Community Cloud.
3. Click **New app** → select your repo.
4. Choose:
   - **Main file**: `app.py`
   - **Branch**: `main` or `master`
5. Deploy.


> **Live App:** https://8crgf4pntr53g5gcbnb55x.streamlit.app

---

## Author (Fill this in)

- **Student Name**: Hemer Pandya 
- **Candidate Registration Number**: n/a
- **CRS Name**: Artificial Intelligence  
- **Course Name**: Mathematics for AI – II  
- **School Name**: udgam school for children 
