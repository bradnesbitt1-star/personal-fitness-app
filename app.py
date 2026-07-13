import streamlit as st

st.set_page_config(page_title="Personal Fitness App", layout="centered")

st.title("🏋️ Personal Fitness Planner")

st.header("Your Information")

age = st.number_input("Age", min_value=10, max_value=100, value=30)
sex = st.selectbox("Sex", ["Male", "Female"])
weight = st.number_input("Weight (lbs)", min_value=50, max_value=500, value=180)
height = st.number_input("Height (inches)", min_value=48, max_value=90, value=70)

activity_level = st.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active",
        "Athlete"
    ]
)

goal = st.selectbox(
    "Goal",
    [
        "Lose Fat",
        "Maintain",
        "Build Muscle"
    ]
)

def calculate_bmr(age, sex, weight, height):
    weight_kg = weight * 0.453592
    height_cm = height * 2.54
    
    if sex == "Male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def activity_multiplier(level):
    return {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Athlete": 1.9
    }[level]

if st.button("Calculate Plan"):

    bmr = calculate_bmr(age, sex, weight, height)
    tdee = bmr * activity_multiplier(activity_level)

    if goal == "Lose Fat":
        calories = tdee - 500
    elif goal == "Build Muscle":
        calories = tdee + 300
    else:
        calories = tdee

    protein = weight * 0.8
    fat = weight * 0.35
    carbs = (calories - (protein * 4 + fat * 9)) / 4

    st.subheader("📊 Your Results")
    st.write(f"**BMR:** {round(bmr)} calories/day")
    st.write(f"**TDEE:** {round(tdee)} calories/day")
    st.write(f"**Target Calories:** {round(calories)} per day")

    st.subheader("🍽 Macronutrients")
    st.write(f"Protein: {round(protein)} g")
    st.write(f"Fat: {round(fat)} g")
    st.write(f"Carbs: {round(carbs)} g")

st.divider()

st.header("📈 Weekly Progress Check")

weekly_change = st.number_input("Weekly Weight Change (lbs)", value=0.0)

if st.button("Adjust Calories"):

    if goal == "Lose Fat":
        if weekly_change > -0.5:
            st.warning("Fat loss too slow. Reduce calories by 200.")
        elif weekly_change < -1.5:
            st.warning("Losing too fast. Increase calories by 200.")
        else:
            st.success("You're on track!")

    elif goal == "Build Muscle":
        if weekly_change < 0.25:
            st.warning("Gaining too slow. Increase calories by 200.")
        elif weekly_change > 1:
            st.warning("Gaining too fast. Reduce calories by 200.")
        else:
            st.success("You're on track!")

    else:
        st.info("Maintenance goal selected.")
