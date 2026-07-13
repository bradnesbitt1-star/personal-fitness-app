import streamlit as st

st.set_page_config(page_title="Personal Fitness Coach", layout="centered")

st.title("🏋️ Personal Fitness Coach")

st.header("Tell Me About You")

goal = st.selectbox(
    "Primary Goal",
    ["Lose Fat", "Build Muscle", "Improve General Fitness"]
)

experience = st.selectbox(
    "Experience Level",
    ["Beginner", "Intermediate", "Advanced"]
)

days = st.slider("How many days per week can you train?", 2, 6, 3)

equipment = st.selectbox(
    "Equipment Access",
    ["Gym", "Dumbbells Only", "Bodyweight Only"]
)

def generate_plan(goal, experience, days, equipment):
    plan = {}

    if days <= 3:
        split = ["Full Body"] * days
    elif days == 4:
        split = ["Upper Body", "Lower Body", "Upper Body", "Lower Body"]
    else:
        split = ["Push", "Pull", "Legs", "Upper", "Lower"][:days]

    for i, day in enumerate(split):
        if equipment == "Gym":
            exercises = [
                "Squats",
                "Bench Press",
                "Deadlifts",
                "Pull-ups",
                "Shoulder Press"
            ]
        elif equipment == "Dumbbells Only":
            exercises = [
                "Goblet Squats",
                "Dumbbell Bench Press",
                "Dumbbell Rows",
                "Dumbbell Shoulder Press",
                "Lunges"
            ]
        else:
            exercises = [
                "Push-ups",
                "Bodyweight Squats",
                "Plank",
                "Lunges",
                "Glute Bridges"
            ]

        if experience == "Beginner":
            sets_reps = "3 sets of 8–12 reps"
        elif experience == "Intermediate":
            sets_reps = "4 sets of 6–10 reps"
        else:
            sets_reps = "4–5 sets of 4–8 reps"

        plan[f"Day {i+1} - {day}"] = {
            "Exercises": exercises,
            "Prescription": sets_reps
        }

    return plan

if st.button("Generate My Workout Plan"):

    workout_plan = generate_plan(goal, experience, days, equipment)

    st.header("📅 Your Weekly Plan")

    for day, details in workout_plan.items():
        st.subheader(day)
        st.write(f"**Prescription:** {details['Prescription']}")
        for exercise in details["Exercises"]:
            st.write(f"- {exercise}")

    st.divider()

    st.subheader("📈 Progression Rule")
    st.write("When you hit the top of the rep range for all sets, increase weight next week.")
