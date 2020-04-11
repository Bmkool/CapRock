"""
CapRock_drink.py - Class to hold information of a drink

@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 4/10/2020
"""
import CapRock_backend_util as util
import CapRock_liquid as liquid

# Position Constants
LIQUID_POS = 0
VOLUME_POS = 1

class Drink():
    """
    All information necessary to create a drink and what liquids it contains.
    Params:
    name (string) - Name of liquid
    1-4 liquid_info (liquid_obj, float) - Liquid tuple (liquid, volume in oz)
    """

    def __init__(self, name, *liquid_info):
        """
        Constructor for drink class.
        """
        if len(liquid_info) > util.MAX_LIQ_PER_DRINK:
            raise util.CapRockError("Max %d liquids in a drink!" % util.MAX_LIQ_PER_DRINK)
        if len(liquid_info) == 0:
            raise util.CapRockError("Must include at least one liquid!")
        if len(name) > util.DRINK_MAX_LEN:
            raise util.CapRockError("Name greater than %d characters" % util.DRINK_MAX_LEN)
        self._liquids = []
        self._name = name
        self._total_volume = 0

        # Add each liquid to drink
        for liq in liquid_info:
            if len(liq) != 2 or not isinstance(liq[LIQUID_POS], liquid.Liquid):
                raise util.CapRockError("Liquid must be tuple (liquid_obj, volume)")

            self._liquids.append(liq) # Add to drink list

        self._update_drink_info()

    def get_name(self):
        """ Returns the Name of the drink """
        return self._name

    def change_name(self, new_name):
        """ Changes the Name of the drink to new_name """
        if len(new_name) > util.DRINK_MAX_LEN:
            raise util.CapRockError("Name greater than %d characters" % util.DRINK_MAX_LEN)

        self._name = new_name

    def get_liquids_obj(self):
        """ Returns all the liquids as a list of tuples (liquid_obj, volume) """
        liquid_list = []
        for liq in self._liquids:
            liquid_list.append((liq[LIQUID_POS], liq[VOLUME_POS]))
        return liquid_list

    def get_liquids_name(self):
        """ Returns all the liquids as a list of tuples (liquid_str_name, volume) """
        liquid_list = []
        for liq in self._liquids:
            liquid_list.append((liq[LIQUID_POS].get_name(), liq[VOLUME_POS]))
        return liquid_list

    def get_abv(self):
        """ Returns the abv of the drink """
        return self._abv

    def get_volume(self):
        """ Returns the volume of the drink """
        return self._total_volume

    def _update_drink_info(self):
        """ Updates the ABV and volume based on current liquids in drink """
        abv_sum = 0
        for liq in self._liquids:
            abv_sum = abv_sum + (liq[LIQUID_POS].get_abv()*liq[VOLUME_POS])
            self._total_volume = self._total_volume + liq[VOLUME_POS]

        self._abv = abv_sum/self._total_volume

    def add_liquid(self, liquid_info):
        """ Adds liquid info (liquid_obj, oz) to a drink """
        if len(liquid_info) == util.MAX_LIQ_PER_DRINK:
            raise util.CapRockError("Max %d liquids in a drink!" % util.MAX_LIQ_PER_DRINK)

        if len(liquid_info) != 2 or not isinstance(liquid_info[LIQUID_POS], liquid.Liquid):
            raise util.CapRockError("Liquid must be tuple (liquid_obj, volume)")

        self._liquids.append(liquid_info)
        self._update_drink_info()

    def remove_liquid(self, liquid):
        """
        Removes liquid from drink
        @param liquid (string): name of liquid to remove
        """

        for liq in self._liquids:
            if liquid.lower() == liq[LIQUID_POS].get_name().lower():
                self._liquids.remove(liq)
                self._update_drink_info()
                return
        raise util.CapRockError("Liquid not currently in drink!")

    def get_drink_info(self):
        """
        Returns dict of all drink info
        (name, abv, liquids, total_volume)
        """
        return {"name":self.get_name(), "abv":self.get_abv(), "liquids":self.get_liquids_name(),
                "total_volume":self.get_volume()}