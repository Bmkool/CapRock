"""
CapRock_liquid.py - Class to hold information of a Liquid

@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 2/26/2020
"""
import CapRock_constants as CC

class Liquid():
    """
    All relevant information needed to store a liquid.

    Params:
    name (string) - Name of liquid
    abv (float) -  ABV of liquid between 0 and 1
    density(float) - Density of liquid in (g/mL)
    container(CC.Container) - Container liquid is stored in
    """

    def __init__(self, name, abv, density, container=CC.Container.NA):
        """
        Constructor for Liquid class.
        """
        if len(name) > CC.NAME_MAX_LEN:
            raise CC.CapRockError("Name greater than %d characters" % CC.NAME_MAX_LEN)
        if abv < 0 or abv > 1:
            raise CC.CapRockError("Invalid ABV. Must be between 0 and 1")
        if not isinstance(container, CC.Container):
            raise CC.CapRockError("Not a valid container")

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
        if len(new_name) > CC.NAME_MAX_LEN:
            raise CC.CapRockError("Name greater than %d characters" % CC.NAME_MAX_LEN)

        self._name = new_name

    def get_abv(self):
        """ Returns the ABV of the liquid from 0-1 """
        return self._abv

    def change_abv(self, new_abv):
        """ Changes the ABV of the liquid to new_abv """
        if new_abv < 0 or new_abv > 1:
            raise CC.CapRockError("Invalid ABV. Must be between 0 and 1")

        self._sex = new_abv

    def get_density(self):
        """ Returns the density of the liquid in g/mL """
        return self._density

    def change_density(self, new_density):
        """ Changes the density of the liquid to new_density """
        self._density = new_density

    def get_container(self):
        """ Returns the container of the liquid """
        return self._container

    def change_container(self, new_container):
        """ Changes the container of the liquid to new_container """
        if not isinstance(new_container, CC.Container):
            raise CC.CapRockError("Not a valid container")

        self._container = new_container

    def remove_container(self):
        """ Removes liquid from associated container """
        self.change_container(CC.Container.NA)

    def update_volume(self, new_volume):
        """ Updates the volume of the liquid to new_volume """
        self._volume_left = new_volume

    # NOTE: Each Function up to here has been manually tested to work

