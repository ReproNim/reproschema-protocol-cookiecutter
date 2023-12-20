import json
import os
import shutil

def get_pref_label(activity_path):
    try:
        with open(activity_path, 'r') as file:
            activity_schema = json.load(file)
        return activity_schema.get("prefLabel", "Unknown Activity")
    except (FileNotFoundError, json.JSONDecodeError):
        return "Unknown Activity"

def update_json_schema(activities, base_path):
    schema_file = os.path.join(base_path, '{{ cookiecutter.__protocol_slug }}/{{ cookiecutter.__protocol_slug }}_schema')  # Update with the correct relative path
    with open(schema_file, 'r') as file:
        schema = json.load(file)

    # Clear existing activities in ui and order
    schema['ui']['addProperties'] = []
    schema['ui']['order'] = []

    # Update ui and order based on available activities
    for activity in activities:
        activity_schema_path = os.path.join(base_path, f'activities/{activity}/{activity}_schema')
        pref_label = get_pref_label(activity_schema_path)
        activity_path = f"../activities/{activity}/{activity}_schema"

        schema['ui']['addProperties'].append({
            "isAbout": activity_path,
            "variableName": f"{activity}_schema",
            "prefLabel": pref_label
        })
        schema['ui']['order'].append(activity_path)

    # Save the updated schema
    with open(schema_file, 'w') as file:
        json.dump(schema, file, indent=4)

def main():
    base_path = os.getcwd()  # Base path of the generated project
    activities_path = os.path.join(base_path, 'activities')

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

    # Update the JSON schema
    activities = [activity for activity in selected_activities if os.path.exists(os.path.join(activities_path, activity))]
    update_json_schema(activities, base_path)

if __name__ == "__main__":
    main()