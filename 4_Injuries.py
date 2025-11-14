import math
from datetime import date
import pandas as pd
import streamlit as st
from common import auth_guard, inject_dark_theme, sql_df, call_proc, null_or

st.set_page_config(page_title="Injuries · Sports Analytics", page_icon="🩹", layout="wide")
inject_dark_theme()
auth_guard()

st.title("🩹 Injuries")

c1, c2, c3, c4 = st.columns(4)

teams = sql_df("SELECT team_id, team_name FROM Teams ORDER BY team_name")
team_map = {r.team_name: r.team_id for _, r in teams.iterrows()}
team_choice = c1.selectbox("Team", ["All"] + list(team_map.keys()))
team_id = None if team_choice == "All" else team_map[team_choice]

status_choice = c2.selectbox("Status", ["All", "Fit", "Injured", "Recovering", "Doubtful"])
only_active = c3.checkbox("Only active injuries", value=True)
q = c4.text_input("Search player")

inj = sql_df("SELECT * FROM v_injury_summary")
inj["status_norm"] = inj["status"].fillna("").str.strip().str.lower()

if only_active:
    inj = inj[inj["status_norm"] == "injured"]

if team_id:
    team_name = [name for name, tid in team_map.items() if tid == team_id][0]
    inj = inj[inj["team_name"] == team_name]

if status_choice != "All":
    inj = inj[inj["status_norm"] == status_choice.lower()]

if q:
    inj = inj[inj["player_name"].str.contains(q, case=False, na=False)]

if st.session_state.user.get("role") == "admin":
    with st.expander("➕ Add injury"):
        with st.form("add_injury"):
            players = sql_df("SELECT player_id, name FROM Players ORDER BY name")
            pmap = {r.name: r.player_id for _, r in players.iterrows()}

            g1, g2, g3 = st.columns(3)
            psel = g1.selectbox("Player*", list(pmap.keys()) if pmap else [])
            itype = g2.text_input("Injury type*", placeholder="Hamstring")
            idate = g3.date_input("Injury date*", value=date.today())

            h1, h2 = st.columns(2)
            expected = h1.date_input("Expected return", value=None)
            status = h2.selectbox("Status", ["Injured", "Recovering", "Doubtful", "Fit"])

            if st.form_submit_button("Add"):
                ok = call_proc(
                    "add_injury",
                    p_player_id=pmap.get(psel),
                    p_injury_type=itype or None,
                    p_injury_date=str(idate),
                    p_expected_return=str(expected) if expected else None,
                    p_status=status or None
                )
                if ok:
                    st.success("Injury added.")
                    st.rerun()

if inj.empty:
    st.info("No injuries to show.")
else:
    n_cols = 3
    n_rows = math.ceil(len(inj) / n_cols)

    for r in range(n_rows):
        cols = st.columns(n_cols)
        for i, col in enumerate(cols):
            ix = r * n_cols + i
            if ix >= len(inj):
                break

            row = inj.iloc[ix]
            status_chip = row.get("status") or "-"
            chip_bg = {
                "injured": "rgba(255,77,109,0.15)",
                "recovering": "rgba(255,200,87,0.15)",
                "doubtful": "rgba(255,200,87,0.15)",
                "fit": "rgba(80,227,194,0.15)"
            }.get(str(status_chip).lower(), "rgba(255,255,255,0.06)")

            with col:
                st.markdown(
                    f"""
                    <div class="app-card">
                        <div class="title-20">{row.get('player_name','Unknown')}</div>
                        <span class="app-badge">{row.get('team_name') or 'No Team'}</span>
                        <div class="muted">Type: <b>{row.get('injury_type') or '-'}</b></div>
                        <div class="muted">Injured: <b>{row.get('injury_date') or '-'}</b></div>
                        <div class="muted">Expected: <b>{row.get('expected_return') or '-'}</b></div>
                        <div style="margin-top:8px; display:inline-block; padding:6px 10px; border-radius:8px; background:{chip_bg};">
                            <b>Status:</b> {status_chip}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
