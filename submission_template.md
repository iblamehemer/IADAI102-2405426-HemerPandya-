
# Player Injuries & Team Performance Dashboard – Submission Document

## 1. GitHub Repository Link

GitHub Link: https://github.com/<your-username>/<IADAI102(Student_ID)-YourName>

---

## 2. Student Details

- **Student’s Full Name:** <Your Full Name>  
- **Candidate Registration Number:** <Your Candidate Number>  
- **CRS Name:** Artificial Intelligence  
- **Course Name:** Mathematics for AI – II  
- **School Name:** <Your School Name>  

---

## 3. Scenario Selected

**Scenario 1: Player Injuries and Team Performance Dashboard**

---

## 4. Research Questions

1. How do key player injuries affect their team’s performance (win/draw/loss ratio and goal difference) during their absence?
2. Which clubs experience the largest performance drop during injury periods of their top players?
3. How do players’ performance ratings change before and after returning from injury (who improves vs declines)?
4. Are there specific months or parts of the season where injury frequency is significantly higher across clubs?
5. Is there a relationship between player age and the severity of performance change during injury spells?

---

## 5. Understanding the Problem

(Write 1–2 short paragraphs in your own words about FootLens Analytics, what they want, and how your dashboard helps make data-driven decisions.)

---

## 6. Data Preprocessing & Cleaning

Brief points describing what you did, for example:

- Loaded the dataset using Pandas.
- Converted `match_date`, `injury_start_date`, and `injury_end_date` columns to datetime.
- Cleaned missing and invalid values in `rating`, `goals_for`, `goals_against`, and `age`.
- Created new features:
  - `goal_diff = goals_for - goals_against`
  - `points` based on match result (W=3, D=1, L=0)
  - `injury_phase` (Pre-Injury, During Injury, Post-Injury)
  - `avg_rating_pre_injury`, `avg_rating_post_injury`, `rating_change`
  - `performance_drop_index` at team level.

(You can add screenshots of your code or outputs here if needed.)

---

## 7. Exploratory Data Analysis & Insights

Summarise key insights, for example:

- Top clubs with the highest performance drop during injury spells.
- Players with the most injury incidents.
- Players who improved vs declined after injury.
- Months with highest injury concentration.
- Patterns between age and rating change.

(Add bullet points and/or screenshots of important charts.)

---

## 8. Dashboard Visualization & Design

Describe the main charts in your Streamlit app:

1. Bar Chart – Teams with Highest Performance Drop
2. Line Chart – Player Rating Timeline Around Injury
3. Heatmap – Injury Frequency Across Months and Clubs
4. Scatter Plot – Age vs Rating Change
5. Leaderboard Table – Comeback Players by Rating Improvement

Explain briefly how these charts help technical staff understand the impact of injuries.

---

## 9. GitHub & Streamlit Deployment

- GitHub repository created with `app.py`, `requirements.txt`, and `README.md`.
- Streamlit app deployed using Streamlit Cloud.
- Live dashboard link: https://your-streamlit-app-link.streamlit.app/

---

## 10. Conclusion / Reflection

(Write a short paragraph about what you learned from this project — about using Python/Streamlit and how analytics can support football decision-making.)
