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

last_output = []


def find_Riven(endpoint):
    all_auctions = []
    stat_list = stat[:]

    if Settings.randomize_stats:
        random.shuffle(stat_list)
        print("[INFO] Stat list randomized")

    for s in stat_list:
        print("Trying Attribute: " + s)

        if Settings.request_mode == "fast":
            delay = random.uniform(0.3, 0.35)
        else:
            delay = random.uniform(6, 7)

        time.sleep(delay)

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

            print(f"Rivens Found: {len(auctions)} | Total: {len(all_auctions)}")
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


def run_riven_search():
    global last_output

    print(f"\nFinding Riven Mods... Mode: {Settings.request_mode.upper()} (Please Be Patient)\n")

    find_Riven("/auctions/search?type=riven")

    output = RivenMod.parse_scraped_data()

    if isinstance(output, list):
        last_output = output
        for r in output:
            print(r)
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
            key=lambda r: (r.calculated_value / r.plat if r.plat != 0 else 0),
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


def settings_menu():
    while True:
        print("\n=== Settings ===")
        print(f"1. Set Preferred Status ({Settings.prefered_status or 'ALL'})")
        print(f"2. Toggle Randomize Stat List ({Settings.randomize_stats})")
        print(f"3. Set Minimum Endo/Plat ({Settings.min_endo_per_plat})")
        print(f"4. Set Request Mode ({Settings.request_mode})")
        print("5. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            print("\nChoose status:")
            print("1. ALL")
            print("2. online")
            print("3. ingame")
            print("4. offline")

            s = input("Choice: ").strip()

            if s == "1":
                Settings.prefered_status = ""
            elif s == "2":
                Settings.prefered_status = "online"
            elif s == "3":
                Settings.prefered_status = "ingame"
            elif s == "4":
                Settings.prefered_status = "offline"
            else:
                print("Invalid choice")
                continue

            Settings.save_settings()

        elif choice == "2":
            Settings.randomize_stats = not Settings.randomize_stats
            Settings.save_settings()

        elif choice == "3":
            try:
                val = float(input("Enter value: "))
                Settings.min_endo_per_plat = val
                Settings.save_settings()
            except:
                print("Invalid input")

        elif choice == "4":
            print("\nRequest Mode:")
            print("1. fast (0.3-0.35 sec)")
            print("2. safe (6-8 sec)")

            mode = input("Choice: ").strip()

            if mode == "1":
                Settings.request_mode = "fast"
            elif mode == "2":
                Settings.request_mode = "safe"
            else:
                print("Invalid choice")
                continue

            Settings.save_settings()

        elif choice == "5":
            break

        else:
            print("Invalid choice")


def main():
    Settings.load_settings()

    print("=== Warframe Riven Scraper ===")

    while True:
        print("\nCommands:")
        print("1. ping")
        print("2. riven")
        print("3. sort")
        print("4. settings")
        print("5. exit")

        command = input("\nEnter command: ").strip().lower()

        if command in ["ping", "1"]:
            print("Pong!")

        elif command in ["riven", "2"]:
            run_riven_search()

        elif command in ["sort", "3"]:
            sort_rivens()

        elif command in ["settings", "4"]:
            settings_menu()

        elif command in ["exit", "5"]:
            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()