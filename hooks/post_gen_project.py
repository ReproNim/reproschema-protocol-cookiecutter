import json
import os
import shutil

def main():
    base_path = os.getcwd()  # Base path of the generated project
    activities_path = os.path.join(base_path, '{{cookiecutter.protocol_name}}', 'activities')

    try:
        with open('selected_activities.json') as f:
            selected_activities = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error reading selected activities.")
        return

    # Create directories for selected activities
    for activity in selected_activities:
        activity_dir = os.path.join(activities_path, activity)
        if not os.path.exists(activity_dir):
            os.makedirs(activity_dir)
            # Copy template files if necessary

    # Optional: Remove unselected activities
    all_activities = ['Activity1', 'Activity2', 'Activity3', 'selectActivity', 'voiceActivity']
    for activity in all_activities:
        if activity not in selected_activities:
            activity_dir = os.path.join(activities_path, activity)
            if os.path.exists(activity_dir):
                shutil.rmtree(activity_dir)

if __name__ == "__main__":
    main()