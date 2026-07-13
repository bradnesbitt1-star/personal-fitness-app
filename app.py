import streamlit as st
from datetime import date, timedelta
import statistics

st.set_page_config(page_title="Aesthetic Transformation Game", layout="centered")

st.title("🔥 10 Week Aesthetic Transformation Game")

# --------------------------
# SESSION STATE INIT
# --------------------------

defaults = {
    "xp": 0,
    "streak": 0,
    "start_date": date.today(),
    "weights": [],
    "waist": [],
    "chest": [],
    "arms": [],
    "calories": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------
# USER STATS
# --------------------------

st.header("Your Stats")

age = st.number_input("Age", 16, 70, 30)
height = st.number_input("Height (inches)", 55, 85, 70)
weight = st.number_input("Current Weight (lbs)", 120, 300, 180)
experience = st.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
effort = st.slider("Effort Level (1–10)", 1, 10, 8)

# --------------------------
# CALORIE CALCULATION
# --------------------------

bmr = 10 * (weight * 0.45) + 6.25 * (height * 2.54) - 5 * age + 5
maintenance = bmr * 1.5

if st.session_state.calories == 0:
    st.session_state.calories = int(maintenance + 200)

st.subheader("🔥 Current Calorie Target")
st.write(f"{st.session_state.calories} kcal/day")
st.write(f"Protein Target: {int(weight)}g/day")

# --------------------------
# AUTO ADJUST CALORIES
# --------------------------

st.subheader("📈 Weekly Weight Check-In")

new_weight = st.number_input("Log Weekly Weight", 120, 300, weight)

if st.button("Submit Weekly Weight"):
    st.session_state.weights.append(new_weight)

    if len(st.session_state.weights) >= 2:
        change = st.session_state.weights[-1] - st.session_state.weights[-2]

        # If gaining too fast (over 0.75 lb/week), reduce calories
        if change > 0.75:
            st.session_state.calories -= 150
            st.warning("⚠️ Gaining too fast. Calories reduced by 150.")

        # If not gaining at all
        elif change < 0.1:
            st.session_state.calories += 150
            st.warning("⚠️ Not gaining. Calories increased by 150.")

        else:
            st.success("✅ Perfect rate of gain.")

# --------------------------
# BODY MEASUREMENTS
# --------------------------

st.subheader("📏 Body Measurements")

waist = st.number_input("Waist (inches)", 20.0, 60.0, 34.0)
chest = st.number_input("Chest (inches)", 30.0, 60.0, 40.0)
arms = st.number_input("Arms (inches)", 10.0, 25.0, 14.0)

if st.button("Log Measurements"):
    st.session_state.waist.append(waist)
    st.session_state.chest.append(chest)
    st.session_state.arms.append(arms)
    st.success("Measurements Saved ✅")

# --------------------------
# TRAINING FREQUENCY
# --------------------------

def calculate_days(experience, effort, age):
    base = 4
    if experience == "Intermediate":
        base = 5
    if experience == "Advanced":
        base = 5
    if effort >= 8:
        base += 1
    if age >= 40:
        base -= 1
    return max(4, min(base, 6))

days_per_week = calculate_days(experience, effort, age)

st.subheader(f"🏋️ Recommended Training Days: {days_per_week}")

# --------------------------
# SPLIT
# --------------------------

split = [
    "Upper Chest + Delts",
    "Lower",
    "Back Width + Arms",
    "Shoulders + Arms",
    "Optional Pump"
][:days_per_week]

st.subheader("Weekly Split")
for i, day in enumerate(split):
    st.write(f"Day {i+1}: {day}")

# --------------------------
# WORKOUT GENERATOR
# --------------------------

exercise_pool = {
    "Upper Chest + Delts": [
        "Incline DB Press 4x6-8",
        "Cable Fly 3x12",
        "Lateral Raises 4x15",
        "Overhead Tricep Extension 3x12"
    ],
    "Lower": [
        "Squats 4x6",
        "RDL 3x8",
        "Leg Press 3x10",
        "Calf Raises 4x12"
    ],
    "Back Width + Arms": [
        "Pullups 4x8",
        "Chest Supported Row 4x8",
        "Cable Curl 3x12",
        "Face Pull 3x15"
    ],
    "Shoulders + Arms": [
        "DB Shoulder Press 4x8",
        "Lateral Raises 4x15",
        "Barbell Curl 3x10",
        "Pushdowns 3x12"
    ],
    "Optional Pump": [
        "Machine Chest 3x12",
        "Lat Pulldown 3x12",
        "Lateral Raises 4x20",
        "Arm Superset 3 rounds"
    ]
}

st.header("🔥 Today's Workout")

today_index = (date.today().day) % len(split)
today_name = split[today_index]

if "current_workout" not in st.session_state:
    st.session_state.current_workout = exercise_pool[today_name]

st.subheader(today_name)

for ex in st.session_state.current_workout:
    st.write("- " + ex)

# --------------------------
# EXERCISE SWAP BUTTON
# --------------------------

if st.button("🔄 Swap Exercises"):
    st.session_state.current_workout = list(reversed(st.session_state.current_workout))
    st.success("Exercises Swapped 🔥")

# --------------------------
# COMPLETE WORKOUT
# --------------------------

if st.button("✅ Complete Workout"):
    st.session_state.xp += 100
    st.session_state.streak += 1
    st.balloons()
    st.success("🔥 +100 XP — You’re Building Your Best Physique")

# --------------------------
# PROGRESS DASHBOARD
# --------------------------

st.divider()
st.header("🎮 Transformation Stats")

level = st.session_state.xp // 500 + 1

st.write(f"🔥 Streak: {st.session_state.streak}")
st.write(f"⭐ XP: {st.session_state.xp}")
st.write(f"🎮 Level: {level}")

st.progress((st.session_state.xp % 500) / 500)

# --------------------------
# COUNTDOWN
# --------------------------

end_date = st.session_state.start_date + timedelta(weeks=10)
total_days = (end_date - st.session_state.start_date).days
days_passed = (date.today() - st.session_state.start_date).days

st.subheader("⏳ 10 Week Transformation Progress")
st.progress(min(days_passed / total_days, 1))
st.write(f"{days_passed} / {total_days} days complete")

# --------------------------
# MOTIVATION
# --------------------------

st.divider()
st.header("💬 Motivation")

if st.session_state.streak >= 5:
    st.write("You’re not working out. You’re becoming that guy.")
elif st.session_state.streak >= 3:
    st.write("Momentum is forming. Don’t break the chain.")
else:
    st.write("One workout at a time. Identity builds daily.")

