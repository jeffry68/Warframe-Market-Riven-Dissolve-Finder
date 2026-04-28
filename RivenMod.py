import json
import Settings


class RivenMod:

    def __init__(self, name, mastery_rank, mod_rank, rerolls, calculated_value, plat, status, Ingame_name):
        self.name = name
        self.mastery_rank = mastery_rank
        self.mod_rank = mod_rank
        self.rerolls = rerolls
        self.calculated_value = calculated_value
        self.plat = plat
        self.status = status
        self.Ingame_name = Ingame_name

    def __str__(self):
        ratio = int(self.calculated_value / self.plat) if self.plat != 0 else 0
        return f"IGN: {self.Ingame_name}({self.status}), Endo/Plat: {ratio}, Name: {self.name}, Calculated Endo: {self.calculated_value}, Plat: {self.plat}"


def parse_scraped_data():
    count = 0
    result = []

    with open("scraped.txt", "r") as file:
        data = json.load(file)
        auctions = data["payload"]["auctions"]

        for auction in auctions:
            item = auction["item"]

            mastery_rank = item["mastery_level"]
            mod_rank = item["mod_rank"]
            rerolls = item["re_rolls"]
            plat = auction["buyout_price"]

            calculated_value = 100 * (mastery_rank - 8) + 22.5 * 2**mod_rank + 200 * rerolls

            if isinstance(plat, int) and plat != 0:
                ratio = calculated_value / plat

                # ✅ dynamic filter from settings
                if ratio >= Settings.min_endo_per_plat:
                    status = auction["owner"]["status"]

                    if Settings.prefered_status == "" or Settings.prefered_status.lower() == status:
                        count += 1

                        name = item["weapon_url_name"]
                        Ingame_name = auction["owner"]["ingame_name"]

                        riven_mod = RivenMod(
                            name, mastery_rank, mod_rank,
                            rerolls, calculated_value,
                            plat, status, Ingame_name
                        )

                        result.append(riven_mod)

    if count == 0:
        return f"No rivens found matching your filters (Endo/Plat >= {Settings.min_endo_per_plat})"
    else:
        return result