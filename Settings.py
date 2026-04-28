import json
import os

SETTINGS_FILE = "settings.json"

# Default values
prefered_status = ""
min_endo_per_plat = 0
randomize_stats = False


def load_settings():
    global prefered_status, min_endo_per_plat, randomize_stats

    if not os.path.exists(SETTINGS_FILE):
        save_settings()
        return

    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)

        prefered_status = data.get("prefered_status", "")
        min_endo_per_plat = data.get("min_endo_per_plat", 0)
        randomize_stats = data.get("randomize_stats", False)


def save_settings():
    data = {
        "prefered_status": prefered_status,
        "min_endo_per_plat": min_endo_per_plat,
        "randomize_stats": randomize_stats
    }

    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)