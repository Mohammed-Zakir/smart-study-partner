def generate_plan(subjects, hours_per_day, days):
    plan = {}

    if not subjects:
        return {"error": "No subjects provided"}

    # Divide time equally per subject
    per_subject_time = max(1, hours_per_day // len(subjects))

    for day in range(1, days + 1):
        day_key = f"Day {day}"
        plan[day_key] = []

        for subject in subjects:
            plan[day_key].append({
                "subject": subject,
                "duration_hours": per_subject_time
            })

    return plan


def display_plan(plan):
    if "error" in plan:
        print(plan["error"])
        return

    for day, tasks in plan.items():
        print(f"\n📅 {day}")
        print("-" * 20)
        for task in tasks:
            print(f"{task['subject']} → {task['duration_hours']} hrs")


# Example usage
if __name__ == "__main__":
    subjects = ["Math", "Physics", "Chemistry", "English"]
    hours_per_day = 6
    days = 5

    study_plan = generate_plan(subjects, hours_per_day, days)
    display_plan(study_plan)