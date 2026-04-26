import json
import Settings
class RivenMod:

  def __init__(self, name, mastery_rank, mod_rank, rerolls, calculated_value,plat,status,Ingame_name):
    self.name = name
    self.mastery_rank = mastery_rank
    self.mod_rank = mod_rank
    self.rerolls = rerolls
    self.calculated_value = calculated_value
    self.plat = plat
    self.status = status
    self.Ingame_name=Ingame_name

  def __str__(self):
    return f"IGN: {self.Ingame_name}({self.status}), Endo/Plat: {int(self.calculated_value/self.plat)}, Name: {self.name}, Calculated Endo: {self.calculated_value}, Plat: {self.plat}"


def parse_scraped_data():
  count = 0
  result = []
  with open("scraped.txt", "r") as file:
    data = json.load(file)
    auctions = data["payload"]["auctions"]

    for auction in auctions:
      #finding only whats nessesary to calculate
      item = auction["item"]
      mastery_rank = item["mastery_level"]
      mod_rank = item["mod_rank"]
      rerolls = item["re_rolls"]
      plat = auction["buyout_price"]
      

      calculated_value = 100 * (mastery_rank -8) + 22.5 * 2**mod_rank + 200 * rerolls
      if(isinstance(plat, int)):
        if calculated_value/plat > 345:
          status = auction["owner"]["status"]
          #checks to see if the status they wanted was all or just one status
          if (Settings.prefered_status.lower()==""):
            count += 1
            #finding the rest of the values
            name = item["weapon_url_name"]
            Ingame_name=auction["owner"]["ingame_name"]
            #adding all the values to a class
            riven_mod = RivenMod(name, mastery_rank, mod_rank, rerolls,calculated_value, plat, status, Ingame_name)
            result.append(riven_mod)
          elif (Settings.prefered_status.lower()==status):
            count += 1
            #finding the rest of the values
            name = item["weapon_url_name"]
            Ingame_name=auction["owner"]["ingame_name"]
            #adding all the values to a class
            riven_mod = RivenMod(name, mastery_rank, mod_rank, rerolls,calculated_value, plat, status, Ingame_name)
            result.append(riven_mod)
  if count == 0:
    return "Nothing found with an endo per plat ratio of 345 or above (price of buying sculptures) and that match your search paramters."
  else:
    return result

