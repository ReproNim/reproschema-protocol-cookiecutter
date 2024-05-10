# pre_gen_project.py-tpl
import random
import sys
import json


def select_activities(n):
    all_activities = [
        "Activity1",
        "Activity2",
        "Activity3",
        "selectActivity",
        "voiceActivity",
    ]
    return random.sample(all_activities, n)


def main():
    # Read the number of activities from the Cookiecutter context
    num_activities_str = "{{ cookiecutter.number_of_activities }}"

    try:
        num_activities = int(num_activities_str)
        if num_activities <= 0 or num_activities > 5:
            raise ValueError
    except ValueError:
        print("Error: Please enter a number between 1 and 5.")
        sys.exit(1)

    selected_activities = select_activities(num_activities)
    print(f"Selected activities: {', '.join(selected_activities)}")

    # Write the selected activities to a file
    with open("selected_activities.json", "w") as f:
        json.dump(selected_activities, f)


if __name__ == "__main__":
    main()
