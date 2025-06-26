# 🏏 NextGen Cricketer - AI-Powered Talent Evaluator

**NextGen Cricketer** is a Streamlit-based web application that evaluates a cricket player's potential using ODI batting statistics. It uses cosine similarity to compare new player data with elite ODI batsmen, classifying them into categories such as:

- 🌟 Future Top Player  
- 🟡 Promising Talent  
- ⚪ Needs Development  
- 🔴 Not Close Yet

---

## 📌 1. Goal of the Project

The primary goal is to **identify promising ODI batting talent** based on historical performance statistics. The system evaluates a new player’s stats and categorizes them based on their similarity to top-performing players.

📝 _Note: This project currently focuses on ODI **batsmen only**._

---

## 📊 2. Dataset

- Source: [Kaggle – ICC ODI Batting Figures (1971–2019)](https://www.kaggle.com)
- Total Records: 2,589
- Initially 14 columns, cleaned and transformed for modeling.

---

## 🔧 3. Project Workflow

### ➤ Data Cleaning
- Removed players with less than 100 matches.
- Dropped irrelevant columns (`url`, `name`, etc.).
- Renamed columns for clarity.
- Converted country initials to full names.
- Parsed `span` into `start`, `end` and then dropped them after computing duration.

### ➤ Feature Engineering
- `duration`: Career span in years.
- `not out ratio`: Not outs / innings.
- `duck rate`: Ducks / innings.
- `century frequency`: Centuries / innings.
- `conversion rate`: Centuries / (Centuries + Half-centuries).

---

## 🤖 4. Modeling Approach

- Used `MinMaxScaler` for numerical columns.
- Applied `OneHotEncoding` to categorical features.
- Built a preprocessing pipeline using `ColumnTransformer` and `Pipeline`.
- Transformed elite player data using this pipeline.
- For a new player:
  - Stats are transformed using the same pipeline.
  - Cosine similarity is computed with all elite players.
  - An average similarity score is calculated and scaled to a 0–100 range.

---

## 🚀 5. Streamlit Application

- A user-friendly **web interface built with Streamlit**.
- Users input basic stats (matches, innings, runs, etc.).
- Behind the scenes, derived features like ratios and conversion rates are calculated.
- The app returns a simple classification like:
  > “Hey Virat, you are 🌟 Future Top Player!”

---

## 📦 6. Tech Stack

- Python
- Pandas
- Scikit-learn
- Dill
- Streamlit
- Cosine Similarity (for distance measurement)

---

