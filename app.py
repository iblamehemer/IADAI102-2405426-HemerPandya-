import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------- DATA LOADING + FEATURE ENGINEERING ----------

@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)

    # Clean column names (keep original labels for safety)
    df.columns = [c.strip() for c in df.columns]

    # Rename important columns to simpler names
    rename_map = {
        "Name": "player_name",
        "Team Name": "team",
        "Age": "age",
        "FIFA rating": "fifa_rating",
        "Injury": "injury_type",
        "Date of Injury": "date_of_injury",
        "Date of return": "date_of_return",
    }
    df = df.rename(columns=rename_map)

    # Convert dates
    for col in ["date_of_injury", "date_of_return"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Convert numeric-like columns safely
    num_cols = [
        "age",
        "Match1_before_injury_GD",
        "Match2_before_injury_GD",
        "Match3_before_injury_GD",
        "Match1_missed_match_GD",
        "Match2_missed_match_GD",
        "Match3_missed_match_GD",
        "Match1_after_injury_GD",
        "Match2_after_injury_GD",
        "Match3_after_injury_GD",
        "Match1_before_injury_Player_rating",
        "Match2_before_injury_Player_rating",
        "Match3_before_injury_Player_rating",
        "Match1_after_injury_Player_rating",
        "Match2_after_injury_Player_rating",
        "Match3_after_injury_Player_rating",
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Helper: row-wise mean over a list of columns
    def row_mean(row, cols):
        vals = [row[c] for c in cols if c in row.index]
        vals = [v for v in vals if pd.notna(v)]
        return np.mean(vals) if vals else np.nan

    # Player rating: before vs after injury
    df["avg_rating_pre_injury"] = df.apply(
        lambda r: row_mean(
            r,
            [
                "Match1_before_injury_Player_rating",
                "Match2_before_injury_Player_rating",
                "Match3_before_injury_Player_rating",
            ],
        ),
        axis=1,
    )
    df["avg_rating_post_injury"] = df.apply(
        lambda r: row_mean(
            r,
            [
                "Match1_after_injury_Player_rating",
                "Match2_after_injury_Player_rating",
                "Match3_after_injury_Player_rating",
            ],
        ),
        axis=1,
    )
    df["rating_change"] = df["avg_rating_post_injury"] - df["avg_rating_pre_injury"]

    # Team goal difference: before / missed / after
    df["avg_gd_before"] = df.apply(
        lambda r: row_mean(
            r,
            [
                "Match1_before_injury_GD",
                "Match2_before_injury_GD",
                "Match3_before_injury_GD",
            ],
        ),
        axis=1,
    )
    df["avg_gd_during"] = df.apply(
        lambda r: row_mean(
            r,
            [
                "Match1_missed_match_GD",
                "Match2_missed_match_GD",
                "Match3_missed_match_GD",
            ],
        ),
        axis=1,
    )
    df["avg_gd_after"] = df.apply(
        lambda r: row_mean(
            r,
            [
                "Match1_after_injury_GD",
                "Match2_after_injury_GD",
                "Match3_after_injury_GD",
            ],
        ),
        axis=1,
    )

    # Performance drop index for this injury spell (team level, this player)
    df["performance_drop_index"] = df["avg_gd_before"] - df["avg_gd_during"]

    # Team-level aggregation
    if "team" in df.columns:
        team_perf = (
            df.groupby("team")["performance_drop_index"]
            .mean()
            .reset_index()
            .sort_values("performance_drop_index", ascending=False)
        )
    else:
        team_perf = pd.DataFrame()

    return df, team_perf


def build_timeline_df(df: pd.DataFrame) -> pd.DataFrame:
    """Create long-format data for a pre/post injury rating timeline."""
    rows = []
    for _, row in df.iterrows():
        name = row.get("player_name")
        team = row.get("team")
        date_injury = row.get("date_of_injury")

        # pre-injury matches: -3, -2, -1
        mapping = [
            ("Match1_before_injury_Player_rating", -3, "Pre-Injury"),
            ("Match2_before_injury_Player_rating", -2, "Pre-Injury"),
            ("Match3_before_injury_Player_rating", -1, "Pre-Injury"),
            ("Match1_after_injury_Player_rating", 1, "Post-Injury"),
            ("Match2_after_injury_Player_rating", 2, "Post-Injury"),
            ("Match3_after_injury_Player_rating", 3, "Post-Injury"),
        ]

        for col, idx, phase in mapping:
            if col in df.columns:
                rating = row.get(col, np.nan)
                if pd.notna(rating):
                    rows.append(
                        {
                            "player_name": name,
                            "team": team,
                            "rel_match_index": idx,
                            "phase": phase,
                            "rating": rating,
                            "date_of_injury": date_injury,
                        }
                    )

    if rows:
        return pd.DataFrame(rows)
    return pd.DataFrame(
        columns=[
            "player_name",
            "team",
            "rel_match_index",
            "phase",
            "rating",
            "date_of_injury",
        ]
    )

# ---------- STREAMLIT APP UI ----------

def main():
    st.set_page_config(
        page_title="Player Injuries & Team Performance Dashboard",
        layout="wide",
    )

    st.title("⚽ Player Injuries & Team Performance Dashboard")
    st.markdown(
        """
        This dashboard uses the **provided player injuries dataset** to explore:

        - How team goal difference changes when a key player is injured  
        - How player ratings behave before vs after returning  
        - Which clubs and months see more injury incidents  
        - Whether age is linked to performance drop or improvement  
        """
    )

    # Sidebar
    st.sidebar.header("Controls")
    data_file = st.sidebar.text_input(
        "CSV file name",
        value="injuries.csv",
        help="Keep your dataset in the same folder as app.py",
    )

    # Load data
    try:
        df, team_perf = load_data(data_file)
    except FileNotFoundError:
        st.error(f"File '{data_file}' not found. Put it in the same folder as app.py.")
        return
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Build long timeline df
    timeline_df = build_timeline_df(df)

    # Filters
    teams = sorted(df["team"].dropna().unique()) if "team" in df.columns else []
    players = sorted(df["player_name"].dropna().unique()) if "player_name" in df.columns else []

    selected_teams = st.sidebar.multiselect(
        "Filter by Team",
        options=teams,
        default=teams[:3] if teams else [],
    )
    selected_player = st.sidebar.selectbox(
        "Focus Player (Timeline & Comeback)",
        options=["All"] + players,
    )

    # Apply filters
    filtered_df = df.copy()
    if selected_teams:
        filtered_df = filtered_df[filtered_df["team"].isin(selected_teams)]
        timeline_df = timeline_df[timeline_df["team"].isin(selected_teams)]
    if selected_player != "All":
        filtered_df = filtered_df[filtered_df["player_name"] == selected_player]
        timeline_df = timeline_df[timeline_df["player_name"] == selected_player]

    # ---------- KPIs ----------
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Injury Cases", len(df))
    with col2:
        st.metric("Filtered Injury Cases", len(filtered_df))
    with col3:
        avg_drop = filtered_df["performance_drop_index"].mean()
        st.metric("Avg Performance Drop (GD)", f"{avg_drop:.2f}" if pd.notna(avg_drop) else "N/A")
    with col4:
        avg_change = filtered_df["rating_change"].mean()
        st.metric("Avg Rating Change", f"{avg_change:.2f}" if pd.notna(avg_change) else "N/A")

    st.markdown("---")

    # ---------- VISUAL 1: Team performance drop ----------
    st.subheader("1️⃣ Teams with Highest Performance Drop During Injury Spells")
    if not team_perf.empty:
        tp = team_perf.copy()
        if selected_teams:
            tp = tp[tp["team"].isin(selected_teams)]
        fig1 = px.bar(
            tp.head(10),
            x="team",
            y="performance_drop_index",
            title="Top Teams by Avg Performance Drop (Goal Difference)",
            labels={
                "team": "Team",
                "performance_drop_index": "Avg GD Drop (Before vs Missed)",
            },
            text_auto=".2f",
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Team performance data not available.")

    # ---------- VISUAL 2: Player performance timeline ----------
    st.subheader("2️⃣ Player Performance Timeline (Before vs After Injury)")
    if not timeline_df.empty:
        if selected_player == "All":
            st.info("Select a specific player in the sidebar to see their timeline.")
        else:
            fig2 = px.line(
                timeline_df.sort_values("rel_match_index"),
                x="rel_match_index",
                y="rating",
                color="phase",
                markers=True,
                title=f"Rating Around Injury for {selected_player}",
                labels={
                    "rel_match_index": "Relative Match Index (-3,-2,-1,1,2,3)",
                    "rating": "Match Rating",
                    "phase": "Phase",
                },
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Not enough rating data to build a timeline from this dataset.")

    # ---------- VISUAL 3: Injury frequency heatmap ----------
    st.subheader("3️⃣ Injury Frequency by Month and Club")
    if "date_of_injury" in df.columns and "team" in df.columns:
        temp = df.dropna(subset=["date_of_injury", "team"]).copy()
        if not temp.empty:
            temp["injury_month"] = temp["date_of_injury"].dt.to_period("M").dt.to_timestamp()
            heat = (
                temp.groupby(["team", "injury_month"])["player_name"]
                .nunique()
                .reset_index()
                .rename(columns={"player_name": "injured_players"})
            )
            if selected_teams:
                heat = heat[heat["team"].isin(selected_teams)]
            if not heat.empty:
                fig3 = px.density_heatmap(
                    heat,
                    x="injury_month",
                    y="team",
                    z="injured_players",
                    color_continuous_scale="Reds",
                    title="Injury Clusters Across Months and Teams",
                    labels={
                        "injury_month": "Month",
                        "team": "Team",
                        "injured_players": "Number of Injured Players",
                    },
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No injury records for the selected teams/time range.")
        else:
            st.info("No valid injury dates in the dataset.")
    else:
        st.info("Missing 'Date of Injury' or 'Team Name' in the dataset.")

    # ---------- VISUAL 4: Age vs performance drop ----------
    st.subheader("4️⃣ Age vs Performance Drop Index")
    if "age" in df.columns and "performance_drop_index" in df.columns:
        scatter_df = df[["player_name", "team", "age", "performance_drop_index"]].dropna()
        if selected_teams:
            scatter_df = scatter_df[scatter_df["team"].isin(selected_teams)]
        if not scatter_df.empty:
            fig4 = px.scatter(
                scatter_df,
                x="age",
                y="performance_drop_index",
                hover_name="player_name",
                color="team",
                title="Does Age Influence Performance Drop?",
                labels={
                    "age": "Player Age",
                    "performance_drop_index": "GD Drop (Before - Missed)",
                },
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Not enough data to plot Age vs Performance Drop.")
    else:
        st.info("Age or performance_drop_index not found in dataset.")

    # ---------- VISUAL 5: Comeback leaderboard ----------
    st.subheader("5️⃣ Comeback Leaderboard – Rating Improvement After Injury")
    leaderboard_cols = [
        "player_name",
        "team",
        "injury_type",
        "avg_rating_pre_injury",
        "avg_rating_post_injury",
        "rating_change",
    ]
    if all(c in df.columns for c in leaderboard_cols):
        leaderboard = (
            df[leaderboard_cols]
            .dropna(subset=["rating_change"])
            .sort_values("rating_change", ascending=False)
            .head(20)
        )
        if selected_teams:
            leaderboard = leaderboard[leaderboard["team"].isin(selected_teams)]
        st.dataframe(leaderboard)
    else:
        st.info("Some required columns for the leaderboard are missing.")

    # Raw data
    with st.expander("🔍 Show Raw Filtered Data"):
        st.dataframe(filtered_df)


if __name__ == "__main__":
    main()