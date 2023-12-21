import json
import os
import shutil
import requests

def get_pref_label(activity_path):
    try:
        with open(activity_path, 'r') as file:
            activity_schema = json.load(file)
        return activity_schema.get("prefLabel", "Unknown Activity")
    except (FileNotFoundError, json.JSONDecodeError):
        return "Unknown Activity"

def update_json_schema(activities, base_path):
    schema_file = os.path.join(base_path, '{{ cookiecutter.__protocol_slug }}/{{ cookiecutter.__protocol_slug }}_schema')
    with open(schema_file, 'r') as file:
        schema = json.load(file)

    schema['ui']['addProperties'] = []
    schema['ui']['order'] = []

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

    with open(schema_file, 'w') as file:
        json.dump(schema, file, indent=4)

def fetch_latest_checksum(base_path):
    try:
        # Using Python requests to fetch and parse JSON
        response = requests.get("https://api.github.com/repos/ReproNim/reproschema-ui/commits/master")
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        latest_hash = response.json()['sha']

        config_path = os.path.join(base_path, 'config.env')
        with open(config_path, 'w') as file:
            file.write(f"REPROSCHEMA_UI_CHECKSUM={latest_hash}\n")

        print("Latest checksum fetched and saved in config.env.")

    except Exception as e:
        print(f"Error fetching checksum: {e}")

def main():
    base_path = os.getcwd()
    init_flag_path = os.path.join(base_path, '.initialized')

    # Check if the project has been initialized before
    if not os.path.exists(init_flag_path):
        # Project initialization logic
        activities_path = os.path.join(base_path, 'activities')

        try:
            with open('selected_activities.json') as f:
                selected_activities = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error reading selected activities.")
            return

        for activity in selected_activities:
            activity_dir = os.path.join(activities_path, activity)
            if not os.path.exists(activity_dir):
                os.makedirs(activity_dir)

        all_activities = ['Activity1', 'Activity2', 'Activity3', 'selectActivity', 'voiceActivity']
        for activity in all_activities:
            if activity not in selected_activities:
                activity_dir = os.path.join(activities_path, activity)
                if os.path.exists(activity_dir):
                    shutil.rmtree(activity_dir)

        activities = [activity for activity in selected_activities if os.path.exists(os.path.join(activities_path, activity))]
        update_json_schema(activities, base_path)

        # Mark initialization as complete
        with open(init_flag_path, 'w') as f:
            f.write('initialized')

    # Fetch and save the latest checksum
    fetch_latest_checksum(base_path)

if __name__ == "__main__":
    main()