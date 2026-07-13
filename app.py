import streamlit as st
import sqlite3
from datetime import date, datetime, timedelta

st.set_page_config(page_title="ADHD Fitness System", layout="centered")

# -----------------------
# Database Setup
# -----------------------

conn = sqlite3.connect("fitness.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT PRIMARY KEY,
    xp INTEGER,
    streak INTEGER,
    total_workouts INTEGER,
    last_workout TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS workouts (
    name TEXT,
    workout_date TEXT
)
""")

conn.commit()

# -----------------------
# User Selection
# -----------------------

st.title("🔥 ADHD Fitness System")

user_name = st.text_input("Enter Your Name")

if user_name:

    c.execute("SELECT * FROM users WHERE name=?", (user_name,))
    user = c.fetchone()

    if not user:
        c.execute("INSERT INTO users VALUES (?, 0, 0, 0, NULL)", (user_name,))
        conn.commit()
        c.execute("SELECT * FROM users WHERE name=?", (user_name,))
        user = c.fetchone()

    xp, streak, total_workouts, last_workout = user[1], user[2], user[3], user[4]

    # -----------------------
    # Workout Logging
    # -----------------------

    st.subheader("Today's Workout")

    workout_type = st.selectbox(
        "What did you train?",
        ["Full Body", "Upper Body", "Lower Body", "Cardio", "Mobility"]
    )

    if st.button("✅ Log Workout"):

        today = date.today()
        xp += 50
        total_workouts += 1

        if last_workout:
            last_date = datetime.strptime(last_workout, "%Y-%m-%d").date()
            if (today - last_date).days <= 2:
                streak += 1
            else:
                streak = 1
        else:
            streak = 1

        last_workout = str(today)

        c.execute("UPDATE users SET xp=?, streak=?, total_workouts=?, last_workout=? WHERE name=?",
                  (xp, streak, total_workouts, last_workout, user_name))
        c.execute("INSERT INTO workouts VALUES (?, ?)", (user_name, today))
        conn.commit()

        st.success("🔥 Workout Logged! +50 XP")
        if streak % 5 == 0:
            st.balloons()

    # -----------------------
    # Progress Dashboard
    # -----------------------

    st.divider()
    st.header("📊 Progress")

    level = xp // 500 + 1

    st.write(f"🔥 Streak: {streak}")
    st.write(f"🏆 Total Workouts: {total_workouts}")
    st.write(f"⭐ XP: {xp}")
    st.write(f"🎮 Level: {level}")

    st.progress((xp % 500) / 500)

    # -----------------------
    # Weekly Goal
    # -----------------------

    st.divider()
    st.header("🎯 Weekly Goal")

    one_week_ago = date.today() - timedelta(days=7)
    c.execute("SELECT COUNT(*) FROM workouts WHERE name=? AND workout_date>=?",
              (user_name, str(one_week_ago)))
    weekly_count = c.fetchone()[0]

    st.write(f"Workouts this week: {weekly_count}/3")

    if weekly_count >= 3:
        st.success("✅ Weekly Goal Complete! Reward yourself.")
    else:
        st.info("3 workouts per week unlocks your weekly reward.")

    # -----------------------
    # Badges
    # -----------------------

    st.divider()
    st.header("🏅 Badges")

    if streak >= 5:
        st.write("🔥 5-Day Streak Badge")
    if total_workouts >= 20:
        st.write("💪 20 Workout Milestone")
    if level >= 5:
        st.write("🚀 Level 5 Achieved")

    if streak < 5 and total_workouts < 20 and level < 5:
        st.write("No badges yet — keep building momentum!")

    # -----------------------
    # Simple Workout Plan
    # -----------------------

    st.divider()
    st.header("📅 Suggested Workout Plan")

    days = st.slider("Days per week", 2, 5, 3)

    if days <= 3:
        split = ["Full Body"] * days
    elif days == 4:
        split = ["Upper", "Lower", "Upper", "Lower"]
    else:
        split = ["Push", "Pull", "Legs", "Upper", "Lower"]

    for i, day in enumerate(split):
        st.write(f"Day {i+1}: {day}")

    st.divider()

    # -----------------------
    # Motivation
    # -----------------------

    st.header("💬 Motivation")

    if streak >= 5:
        st.write("You're building identity-based consistency.")
    elif streak >= 2:
        st.write("Momentum is forming. Keep showing up.")
    else:
        st.write("Just one workout today. That's it.")
