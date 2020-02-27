"""
CapRock_liquid.py - Class to hold information of a Liquid

@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 2/26/2020
"""
import CapRock_util as CU

class Liquid():
    """
    All relevant information needed to store a liquid.

    Params:
    name (string) - Name of liquid
    abv (float) -  ABV of liquid between 0 and 1
    density(float) - Density of liquid in (g/mL)
    container(CU.Container) - Container liquid is stored in
    """

    def __init__(self, name, abv, density, container=CU.Container.NA):
        """
        Constructor for Liquid class.
        """
        if len(name) > CU.NAME_MAX_LEN:
            raise CU.CapRockError("Name greater than %d characters" % CU.NAME_MAX_LEN)
        if abv < 0 or abv > 1:
            raise CU.CapRockError("Invalid ABV. Must be between 0 and 1")
        if not isinstance(container, CU.Container):
            raise CU.CapRockError("Not a valid container")

        self._name = name
        self._abv = abv
        self._density = density
        self._container = container
        self._volume_left = 0

    def get_name(self):
        """ Returns the Name of the liquid """
        return self._name

    def change_name(self, new_name):
        """ Changes the Name of the liquid to new_name """
        if len(new_name) > CU.NAME_MAX_LEN:
            raise CU.CapRockError("Name greater than %d characters" % CU.NAME_MAX_LEN)

        self._name = new_name

    def get_abv(self):
        """ Returns the ABV of the liquid from 0-1 """
        return self._abv

    def change_abv(self, new_abv):
        """ Changes the ABV of the liquid to new_abv """
        if new_abv < 0 or new_abv > 1:
            raise CU.CapRockError("Invalid ABV. Must be between 0 and 1")

        self._abv = new_abv

    def get_density(self):
        """ Returns the density of the liquid in g/mL """
        return self._density

    def change_density(self, new_density):
        """ Changes the density of the liquid to new_density """
        self._density = new_density

    def get_container(self):
        """ Returns the two letter container code of the liquid """
        return self._container.name

    def change_container(self, new_container):
        """ Changes the container of the liquid to new_container """
        if not isinstance(new_container, CU.Container):
            raise CU.CapRockError("Not a valid container")

        self._container = new_container

    def remove_container(self):
        """ Removes liquid from associated container and sets volume to 0 """
        self.change_container(CU.Container.NA)
        self.change_volume_left(0)

    def get_volume_left(self):
        """ Returns the volume of the liquid in oz """
        return self._volume_left

    def change_volume_left(self, new_volume):
        """ Updates the volume of the liquid to new_volume """
        self._volume_left = new_volume

    def get_liquid_info(self):
        """
        Returns dict of all drink info
        (name, abv, density, container, volume_left)
        """
        return {"name":self.get_name(), "abv":self.get_abv(), "density":self.get_density(),
                "container":self.get_container(), "volume_left":self.get_volume_left()}

    # NOTE: Each Function up to here has been manually tested to work

