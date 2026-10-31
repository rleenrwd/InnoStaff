import random

def generate_career_goals(workers, seed, initial_goal_probability):
    if not 0 <= initial_goal_probability <= 1:
        raise ValueError("Initial goal probability must be between zero and one.")

    random_generator = random.Random(seed)

    goal_descriptions = {
    "Operations": "Advance into a more senior operations role.",
    "Software": "Pursue a career in software development.",
    "Network": "Pursue a career in network engineering.",
    "Systems": "Pursue a career in systems administration.",
    "IT": "Pursue a career in information technology support.",
    "Security": "Pursue a career in cybersecurity.",
    "StableEmployment": "Prioritize stable and consistent employment.",
    "Other": "Pursue a career outside the listed families.",
    }

    goal_families = list(goal_descriptions.keys())
    career_goals = []
    career_goal_id = 1

    for worker in workers:
        if random_generator.random() >= initial_goal_probability:
            continue

        goal_family = random_generator.choice(goal_families)

        career_goal = {
            "CareerGoalId": career_goal_id,
            "WorkerId": worker["WorkerId"],
            "RecordedDate": worker["RegisteredDate"],
            "GoalFamily": goal_family,
            "GoalDescription": goal_descriptions[goal_family],
        }

        career_goals.append(career_goal)
        career_goal_id += 1

    return career_goals
