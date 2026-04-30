import json
import os

SETTINGS_FILE = "settings.json"

prefered_status = ""
min_endo_per_plat = 0
randomize_stats = False
request_mode = "safe"


def load_settings():
    global prefered_status, min_endo_per_plat, randomize_stats, request_mode

    if not os.path.exists(SETTINGS_FILE):
        save_settings()
        return

    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)

        prefered_status = data.get("prefered_status", "")
        min_endo_per_plat = data.get("min_endo_per_plat", 0)
        randomize_stats = data.get("randomize_stats", False)
        request_mode = data.get("request_mode", "safe")


def save_settings():
    data = {
        "prefered_status": prefered_status,
        "min_endo_per_plat": min_endo_per_plat,
        "randomize_stats": randomize_stats,
        "request_mode": request_mode
    }

    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)