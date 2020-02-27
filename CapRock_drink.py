"""
CapRock_drink.py - Class to hold information of a drink

@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 2/26/2020
"""
import CapRock_util as CU
import CapRock_liquid as liquid

# Position Constants
LIQUID_POS = 0
VOLUME_POS = 1

class Drink():
    """
    All information necessary to create a drink and what liquids it contains.
    Params:
    name (string) - Name of liquid
    1-4 liquid_info (liquid_obj, int) - Liquid tuple (liquid, volume in oz)
    """

    def __init__(self, name, *liquid_info):
        """
        Constructor for drink class.
        """
        if len(liquid_info) > CU.MAX_LIQ_PER_DRINK:
            raise CU.CapRockError("Max %d liquids in a drink!" % CU.MAX_LIQ_PER_DRINK)
        elif len(liquid_info) == 0:
            raise CU.CapRockError("Must include at least one liquid!")
        self._liquids = []
        self._name = name
        self._total_volume = 0

        # Add each liquid to drink
        abv_sum = 0
        for liq in liquid_info:
            if len(liq) != 2:
                raise CU.CapRockError("Liquid must be tuple (liquid_obj, volume)")
            elif not isinstance(liq[LIQUID_POS], liquid.Liquid):
                raise CU.CapRockError("First parameter in tuple must be liquid_obj")

            abv_sum = abv_sum + (liq[LIQUID_POS].get_abv()*liq[VOLUME_POS])
            self._total_volume = self._total_volume + liq[VOLUME_POS]
            self._liquids.append(liq)

        self._abv = abv_sum/self._total_volume

    def get_name(self):
        """ Returns the Name of the drink """
        return self._name

    def change_name(self, new_name):
        """ Changes the Name of the drink to new_name """
        if len(new_name) > CU.NAME_MAX_LEN:
            raise CU.CapRockError("Name greater than %d characters" % CU.NAME_MAX_LEN)

        self._name = new_name

    def get_liquids(self):
        """ Returns all the liquids as a list of tuples (liquid, volume) """
        all_liquids = []
        for liq in self._liquids:
            all_liquids.append(liq)
        return all_liquids

    def get_abv(self):
        """ Returns the abv of the drink """
        return self._abv

# Testing only
if __name__ == "__main__":
    bourban = liquid.Liquid("bourban", .4, 1, CU.Container.FR)
    rum = liquid.Liquid("151 rum", .755, 1, CU.Container.BR)
    scotch = liquid.Liquid("scotch", .5, 1, CU.Container.FL)
    ss = liquid.Liquid("syrup", 0, 1.2, CU.Container.BL)
    lol = Drink("lul", (bourban, 3), (rum, 4), (ss, 2), (scotch, 3))
    print(lol._abv)
