import requests
import json
import time
import random
import RivenMod
import Settings

baseUrl = "https://api.warframe.market/v1"

stat = [
    "ammo_maximum", "cold_damage", "critical_chance", "critical_damage",
    "base_damage_/_melee_damage", "damage_vs_corpus", "damage_vs_grineer",
    "damage_vs_infested", "electric_damage", "fire_rate_/_attack_speed",
    "heat_damage", "impact_damage", "magazine_capacity", "multishot",
    "projectile_speed", "punch_through", "puncture_damage", "reload_speed",
    "slash_damage", "status_chance", "status_duration", "toxin_damage",
    "recoil", "zoom", "chance_to_gain_extra_combo_count", "combo_duration",
    "critical_chance_on_slide_attack", "finisher_damage",
    "channeling_efficiency", "channeling_damage", "range"
]

user_status = ["online", "ingame", "offline", ""]


last_output = []


def find_Riven(endpoint):
    all_auctions = []

    for s in stat:
        time.sleep(random.uniform(0.3, 0.35))

        params = {
            'platform': 'pc',
            'positive_stats': s,
            'sort_by': 'price_asc',
            'mod_rank': 'maxed'
        }

        response = requests.get(baseUrl + endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            auctions = data["payload"]["auctions"]
            all_auctions.extend(auctions)
        else:
            print("Blocked or bad response:", response.status_code)

    # Deduplicate
    seen_ids = set()
    unique_auctions = []

    for auction in all_auctions:
        auction_id = auction.get("id")
        if auction_id not in seen_ids:
            seen_ids.add(auction_id)
            unique_auctions.append(auction)

    print(f"\nTotal before dedupe: {len(all_auctions)}")
    print(f"Total after dedupe: {len(unique_auctions)}")

    with open("scraped.txt", "w") as f:
        json.dump({"payload": {"auctions": unique_auctions}}, f, indent=4)


def run_riven_search(user_input):
    global last_output

    if user_input != "":
        Settings.prefered_status = user_input

        if Settings.prefered_status.lower() not in user_status:
            print("Unknown parameter, defaulting to all")
            Settings.prefered_status = ""
    else:
        Settings.prefered_status = ""

    print("\nFinding Riven Mods... (Please Be Patient)\n")

    find_Riven("/auctions/search?type=riven")

    output = RivenMod.parse_scraped_data()

    if isinstance(output, list):
        last_output = output

        for riven_mod in output:
            print(riven_mod)
    else:
        print(output)

    print("\nDone!\n")


def sort_rivens():
    global last_output

    if not last_output:
        print("No data to sort. Run 'riven' first.")
        return

    print("\nSort by:")
    print("1. Endo / Plat")
    print("2. Endo")

    choice = input("Choice: ").strip()

    if choice == "1":
        last_output.sort(
            key=lambda r: (
                r.calculated_value / r.plat if r.plat != 0 else 0
            ),
            reverse=True
        )

    elif choice == "2":
        last_output.sort(
            key=lambda r: r.calculated_value,
            reverse=True
        )

    else:
        print("Invalid choice")
        return

    print("\n--- Sorted Results ---\n")
    for r in last_output:
        print(r)


def main():
    print("=== Warframe Riven Scraper ===")

    while True:
        print("\nCommands:")
        print("1. ping")
        print("2. riven [status]      (just typing 2 defaults to ingame)")
        print("3. sort")
        print("4. exit")

        command = input("\nEnter command: ").strip().lower()

        if command == "ping" or command == "1":
            print("Pong!")

        elif command.startswith("riven") or command == "2":
            parts = command.split()
            status = parts[1] if len(parts) > 1 else "ingame"
            run_riven_search(status)

        elif command == "sort" or command == "3":
            sort_rivens()

        elif command == "exit" or command == "4":
            print("Exiting...")
            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()