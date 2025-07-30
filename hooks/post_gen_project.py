import json
import os
import shutil
import requests
import subprocess
import sys
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_pref_label(activity_path):
    """Get preference label from activity schema with proper error handling."""
    try:
        with open(activity_path, "r") as file:
            activity_schema = json.load(file)
        pref_label = activity_schema.get("prefLabel", "Unknown Activity")
        
        # Normalize prefLabel to always return a string
        if isinstance(pref_label, dict):
            # Try to get English label first, then any available language
            normalized = pref_label.get("en", pref_label.get(list(pref_label.keys())[0], "Unknown Activity") if pref_label else "Unknown Activity")
        elif isinstance(pref_label, str):
            normalized = pref_label
        else:
            logger.warning(f"Unexpected prefLabel type in {activity_path}: {type(pref_label)}")
            normalized = "Unknown Activity"
            
        logger.debug(f"Got prefLabel '{normalized}' from {activity_path}")
        return normalized
    except FileNotFoundError:
        logger.warning(f"Activity file not found: {activity_path}")
        return "Unknown Activity"
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {activity_path}: {e}")
        return "Unknown Activity"
    except Exception as e:
        logger.error(f"Unexpected error reading {activity_path}: {e}")
        return "Unknown Activity"


def update_json_schema(activities, base_path):
    schema_file = os.path.join(
        base_path,
        "{{ cookiecutter.__protocol_slug }}/{{ cookiecutter.__protocol_slug }}_schema",
    )
    with open(schema_file, "r") as file:
        schema = json.load(file)

    schema["ui"]["addProperties"] = []
    schema["ui"]["order"] = []

    for activity in activities:
        # Use lowercase schema filename consistently
        activity_schema_filename = f"{activity.lower()}_schema"
        activity_schema_path = os.path.join(
            base_path, f"activities/{activity}/{activity_schema_filename}"
        )
        pref_label = get_pref_label(activity_schema_path)
        activity_path = f"../activities/{activity}/{activity_schema_filename}"

        schema["ui"]["addProperties"].append(
            {
                "isAbout": activity_path,
                "variableName": activity_schema_filename,
                "prefLabel": {"en": pref_label},  # Always use object notation
            }
        )
        schema["ui"]["order"].append(activity_path)

    with open(schema_file, "w") as file:
        json.dump(schema, file, indent=4)


def fetch_latest_checksum(base_path, max_retries=3):
    """Fetch latest UI checksum with retry logic and caching."""
    cache_file = Path(base_path) / ".ui_checksum_cache"
    
    # Check cache first (1 hour validity)
    if cache_file.exists():
        cache_age = time.time() - cache_file.stat().st_mtime
        if cache_age < 3600:  # 1 hour cache
            logger.info("Using cached checksum")
            try:
                with open(cache_file) as f:
                    latest_hash = f.read().strip()
                save_checksum(base_path, latest_hash)
                return True
            except Exception as e:
                logger.warning(f"Failed to read cache: {e}")
    
    # Fetch from GitHub API with retries
    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching latest checksum (attempt {attempt + 1}/{max_retries})")
            response = requests.get(
                "https://api.github.com/repos/ReproNim/reproschema-ui/commits/main",
                timeout=10,
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            response.raise_for_status()
            latest_hash = response.json()["sha"]
            
            # Cache the result
            with open(cache_file, "w") as f:
                f.write(latest_hash)
            
            save_checksum(base_path, latest_hash)
            logger.info("Latest checksum fetched and saved")
            return True
            
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1}")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error on attempt {attempt + 1}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                logger.error("GitHub API rate limit exceeded")
                return False
            logger.warning(f"HTTP error on attempt {attempt + 1}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
    
    logger.error(f"Failed to fetch checksum after {max_retries} attempts")
    return False


def save_checksum(base_path, checksum):
    """Save checksum to config.env file."""
    config_path = Path(base_path) / "config.env"
    try:
        with open(config_path, "w") as file:
            file.write(f"REPROSCHEMA_UI_CHECKSUM={checksum}\n")
        logger.info(f"Checksum saved to {config_path}")
    except Exception as e:
        logger.error(f"Failed to save checksum: {e}")


def setup_pre_commit(optional=True):
    """Set up pre-commit hooks with optional installation."""
    try:
        # Check if pre-commit is already installed
        result = subprocess.run(
            ["pre-commit", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Pre-commit already installed")
        else:
            raise FileNotFoundError("pre-commit not found")
    except FileNotFoundError:
        if optional:
            logger.info("Pre-commit not installed. Run 'pip install pre-commit' to enable hooks")
            return True
        else:
            logger.error("Pre-commit is required but not installed")
            return False
    
    try:
        subprocess.check_call(["pre-commit", "install"], stderr=subprocess.DEVNULL)
        logger.info("Pre-commit hooks installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install pre-commit hooks: {e}")
        return not optional


def main():
    """Main function to handle post-generation setup."""
    base_path = os.getcwd()
    init_flag_path = os.path.join(base_path, ".initialized")

    # Check if the project has been initialized before
    if not os.path.exists(init_flag_path):
        # Project initialization logic
        activities_path = os.path.join(base_path, "activities")

        try:
            with open("selected_activities.json") as f:
                selected_activities = json.load(f)
            logger.info(f"Selected activities: {selected_activities}")
        except FileNotFoundError:
            logger.error("selected_activities.json not found - this file should be created by pre_gen_project.py")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in selected_activities.json: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error reading selected activities: {e}")
            return False

        for activity in selected_activities:
            activity_dir = os.path.join(activities_path, activity)
            if not os.path.exists(activity_dir):
                os.makedirs(activity_dir)

        all_activities = [
            "Activity1",
            "Activity2",
            "Activity3",
            "selectActivity",
            "voiceActivity",
        ]
        for activity in all_activities:
            if activity not in selected_activities:
                activity_dir = os.path.join(activities_path, activity)
                if os.path.exists(activity_dir):
                    shutil.rmtree(activity_dir)

        activities = [
            activity
            for activity in selected_activities
            if os.path.exists(os.path.join(activities_path, activity))
        ]
        try:
            update_json_schema(activities, base_path)
            logger.info("Protocol schema updated successfully")
        except Exception as e:
            logger.error(f"Failed to update protocol schema: {e}")
            return False

        # Mark initialization as complete
        with open(init_flag_path, "w") as f:
            f.write("initialized")

    # Fetch and save the latest checksum
    if not fetch_latest_checksum(base_path):
        logger.warning("Could not fetch latest checksum, using default")
        # Create a default config.env
        config_path = Path(base_path) / "config.env"
        with open(config_path, "w") as f:
            f.write("REPROSCHEMA_UI_CHECKSUM=latest\n")

    # Set up pre-commit (optional)
    setup_pre_commit(optional=True)
    
    # Clean up temporary files
    temp_files = ["selected_activities.json"]
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            logger.debug(f"Removed temporary file: {temp_file}")
        except FileNotFoundError:
            pass
        except Exception as e:
            logger.warning(f"Could not remove {temp_file}: {e}")
    
    logger.info("Post-generation setup completed successfully")
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            logger.error("Post-generation setup failed")
            sys.exit(1)
    except Exception as e:
        logger.critical(f"Critical error in post-generation: {e}")
        sys.exit(1)
