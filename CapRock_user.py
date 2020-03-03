"""
CapRock_user.py - Class to hold information of a user

@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 3/3/2020
"""

import datetime
import CapRock_liquid as liquid
import CapRock_drink as drink
import CapRock_util as CU

TIME_POS = 0
DRINK_POS = 1
OZ_POS = 2

class User():
    """
    All relevant user information to be able to calculate BAC.

    Params:
    name (string) - Name of profile
    sex (CU.Sex enum) - Sex of user
    weight(float) - Weight of user in pounds
    experience(CU.Experience) - How often user drinks
    """
    def __init__(self, name, sex, weight, experience):
        """
        Constructor for user class.
        self._bac (float) - Blood alcohol content
        self._current drinks (list) - (drink_obj, datetime of pour) tuples
        """
        if len(name) > CU.NAME_MAX_LEN:
            raise CU.CapRockError("Name greater than %d characters" % CU.NAME_MAX_LEN)
        if not isinstance(sex, CU.Sex):
            raise CU.CapRockError("Not a valid Sex")
        if not isinstance(experience, CU.Experience):
            raise CU.CapRockError("Not a valid Experience")

        self._name = name
        self._sex = CU.Sex(sex)
        self._weight = weight
        self._experience = experience
        self._bac = 0.0
        self._current_drinks = []

    def get_name(self):
        """ Returns the Name of the user profile """
        return self._name

    def change_name(self, new_name):
        """ Changes the Name of the user profile to new_name """
        if len(new_name) > CU.NAME_MAX_LEN:
            raise CU.CapRockError("Name greater than %d characters" % CU.NAME_MAX_LEN)

        self._name = new_name

    def get_sex(self):
        """ Returns the Sex of the user profile """
        return self._sex.value

    def change_sex(self, new_sex):
        """ Changes the sex of the user profile to new_sex """
        if not isinstance(new_sex, CU.Sex):
            raise CU.CapRockError("Not a valid Sex")

        self._sex = new_sex

    def get_weight(self):
        """ Returns the weight of the user profile in lbs """
        return self._weight

    def change_weight(self,new_weight):
        """ Changes the sex of the user profile to new_weight """
        self._weight = new_weight


    def get_experience(self):
        """ Returns the Experience of the user profile """
        return self._experience.name

    def change_experience(self, new_exp):
        """ Changes the experience of the user profile to new_exp """
        if not isinstance(new_exp, CU.Experience):
            raise CU.CapRockError("Not a valid Experience")

        self._experience = new_exp

    def _calc_bac(self):
        """
        Calculates the BAC of the user based on what when each
        current drink was made. This returns the sum of all individual
        drink's BAC
        """
        bac_sum = 0
        for dr in self._current_drinks:
            # calc time dif in hours
            cur_time = datetime.datetime.now()
            diff = cur_time - dr[TIME_POS]
            hours = diff.total_seconds() / (60*60)
            bac_sum = bac_sum + self._bac_equation(dr[DRINK_POS].get_volume(), dr[DRINK_POS].get_abv(), hours)
        return bac_sum

    def _bac_equation(self, oz_drank, abv, time_elapsed_hr):
        """ Returns estimated bac of single drink """
        # Tested with this example:
        # https://www.craftbeer.com/attachments/0000/1170/Computing_a_BAC_Estimate.pdf
        weight_kg = self._weight/2.2046
        sex_const = CU.MALE_WATER_CONST if self.get_sex() == "Male" else CU.FEMALE__WATER_CONST
        body_water = weight_kg * sex_const * 1000 # to ml
        oz_alc = abv*oz_drank
        gram_alc = 29.57 * oz_alc * .79 # ml/oz for one oz alc * g/mL (density)
        gram_alc_per_ml_water = gram_alc/body_water
        alc_conc_in_blood = gram_alc_per_ml_water * .806 # blood is 80.6% water
        init_bac = alc_conc_in_blood * 100 #g/100 mL
        actual_bac = init_bac - (self._experience.value * time_elapsed_hr)
        if actual_bac < 0:
            actual_bac = 0
        return actual_bac

    def update_bac(self):
        """ Updates the BAC of the user """
        self._bac = self._calc_bac()

    def get_bac(self):
        """ Returns the BAC of the user profile """
        self.update_bac()
        return self._bac

    def add_drink(self, dr):
        """ Adds new drink to current drink list """
        if not isinstance(dr, drink.Drink):
            raise CU.CapRockError("Liquid must be a drink object")

        self._current_drinks.append((datetime.datetime.now(), dr))

    def get_current_drinks(self):
        return self._current_drinks


    def get_user_info(self):
        """
        Returns dict of all drink info
        (name, sex, weight, experience, bac, current_drinks)
        """
        return {"name":self.get_name(), "sex":self.get_sex(), "weight":self.get_weight(),
                "experience":self.get_experience(), "bac":self.get_bac(), "current_drinks":self.get_current_drinks()}


#testing only
if __name__ == "__main__":
    lol = User("hi", CU.Sex.Male, 128, CU.Experience.Light)
    #lol.add_drink(("beer", ))
    print(lol.get_bac())