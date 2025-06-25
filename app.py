import streamlit as st
import pandas as pd
import dill
import gdown
from sklearn.metrics.pairwise import cosine_similarity
import os

# --- Download model from Google Drive if not already downloaded ---
model_path = "/tmp/talent_model.pkl"
file_id = "1FOZLkKQgZ0sVb4wu-MSof9p1Lcz0Zf3t"
url = f"https://drive.google.com/uc?id={file_id}"

# Only download if not already present
if not os.path.exists(model_path):
    gdown.download(url, model_path, quiet=False, use_cookies=False)

# Load the model

with open(model_path, "rb") as f:
    model = dill.load(f)

pipeline = model['pipeline']
elite_transformed = model['elite_data']
country_list = model['countries']


# --- Score Function ---
def score_player(player_df, model_pipeline, model_elite_transformed):
    transformed = model_pipeline.transform(player_df)
    similarity = cosine_similarity(transformed, model_elite_transformed)[0].mean()
    points = round(similarity * 100, 2)
    return points


# --- Classify Function ---
def classify_talent_score(value):
    if value >= 50:
        return '🌟 Future Top Player'
    elif value >= 50:
        return '🟡 Promising Talent'
    elif value >= 35:
        return '⚪ Needs Development'
    else:
        return '🔴 Not Close Yet'


# --- Streamlit App UI ---
st.set_page_config(page_title="Cricket Talent Score", page_icon="🏏", layout="centered")
st.title("🏏 Cricket Player Talent Score")
st.markdown("Enter the player's career stats to evaluate their similarity to elite players.")

# --- Input Form ---
with st.form("player_form"):
    player_name = st.text_input("Player Name")

    col1, col2 = st.columns(2)

    with col1:
        matches = st.number_input("Matches", min_value=1)
        innings = st.number_input("Innings", min_value=1)
        runs = st.number_input("Runs", min_value=0)
        highest_score = st.number_input("Highest Score", min_value=0)
        average = st.number_input("Batting Average", min_value=0.0)
        strike_rate = st.number_input("Strike Rate", min_value=0.0)
        duration = st.number_input("Career Duration (years)", min_value=0.0)
        country = st.selectbox("Country", country_list)

    with col2:
        not_outs = st.number_input("Number of Times Not Out", min_value=0)
        ducks = st.number_input("Number of Ducks (0 runs)", min_value=0)
        centuries = st.number_input("Number of Centuries (100+)", min_value=0)
        half_centuries = st.number_input("Number of Half-Centuries (50–99)", min_value=0)
        balls_faced = st.number_input("Total Balls Faced", min_value=0)

    submit = st.form_submit_button("Evaluate Talent")

# --- Process Input ---
if submit:
    # Derived features
    not_out_ratio = not_outs / innings if innings else 0
    duck_rate = ducks / innings if innings else 0
    century_freq = centuries / innings if innings else 0
    conversion_rate = centuries / (centuries + half_centuries) if (centuries + half_centuries) else 0
    balls_per_innings = balls_faced / innings if innings else 0

    # Create input dataframe
    new_player_data = {
        'matches': [matches],
        'innings': [innings],
        'runs': [runs],
        'highest score': [highest_score],
        'average': [average],
        'strike rate': [strike_rate],
        'country': [country],
        'duration': [duration],
        'not out ratio': [not_out_ratio],
        'duck rate': [duck_rate],
        'century frequency': [century_freq],
        'century conversion rate': [conversion_rate],
        'balls faced per innings': [balls_per_innings]
    }

    new_player = pd.DataFrame(new_player_data)
    score = score_player(new_player, pipeline, elite_transformed)
    classification = classify_talent_score(score)

    # --- Display classification only ---
    st.subheader("🎯 Talent Evaluation")
    st.success(f"Hey **{player_name}**, your class -> **{classification}**!")

    # --- Optional: Show derived metrics ---
    st.markdown("### 📊 Derived Stats (for reference)")
    st.write(f"**Not Out Ratio:** {not_out_ratio:.2f}")
    st.write(f"**Duck Rate:** {duck_rate:.2f}")
    st.write(f"**Century Frequency:** {century_freq:.2f}")
    st.write(f"**Century Conversion Rate:** {conversion_rate:.2f}")
    st.write(f"**Balls Faced per Innings:** {balls_per_innings:.2f}")
