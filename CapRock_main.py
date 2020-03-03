import CapRock_liquid as liquid
import CapRock_drink as drink
import CapRock_user as user
import CapRock_backend_util as util
import logging

def startup():
    try:
        util.init_logging()
        util.load_storage()
    except Exception as e:
        logging.critical("%s - Startup issue" % str(e) )
    return [], [], []
        

def cleanup(profiles, drinks, liquids):
    util.save_storage(profiles, drinks, liquids)




# Testing
if __name__ == "__main__":
    profiles, drinks, liquids = startup()

    profiles.append(user.User("Brian", util.Sex.Male, 165, util.Experience.Heavy))
    profiles.append(user.User("Jim", util.Sex.Male, 150, util.Experience.Light))
    liquids.append(liquid.Liquid("Vodka", .4, .916, util.Container.BL))
    liquids.append(liquid.Liquid("Syrup", 0, .95, util.Container.BR))
    liquids.append(liquid.Liquid("Scotch", .43, .94, util.Container.FL))
    liquids.append(liquid.Liquid("151 rum", .755, .98, util.Container.BR))
    liquids.append(liquid.Liquid("Sprite", 0, 1.037, util.Container.NA))
    drinks.append(drink.Drink("Vodka Sprite", (liquids[0], 1.5), (liquids[4],10.5)))
    drinks.append(drink.Drink("Strong boi", (liquids[0], 1.5), (liquids[1], 1.5), (liquids[2], 2), (liquids[3], 1.5)))
    profiles[0].add_drink(drinks[0])
    profiles[0].add_drink(drinks[1])
    for u in profiles:
        print(u.get_user_info())
    for d in drinks:
        print(d.get_drink_info())
    for l in liquids:
        print(l.get_liquid_info())
    print(profiles[0].get_bac())

    cleanup(profiles, drinks, liquids)
