"""
List of all constants, enums, functions and Exceptions used in CapRock Software
"""
from enum import Enum
import logging
import os
from datetime import datetime
import sys

MAX_LIQ_PER_DRINK = 4
MAX_LIQUIDS_STORED = 64
MAX_DRINKS_STORED = 16
NAME_MAX_LEN = 20
MALE_WATER_CONST = .58
FEMALE__WATER_CONST = .49

class Sex(Enum):
    Male = "Male"
    Female = "Female"

class Experience(Enum):
    """ Absorbtion rate based on type of drinker """
    Light = .012
    Regular = .015
    Heavy = .02

class Container(Enum):
    FL = "Front Left"
    FR = "Front Right"
    BL = "Back Left"
    BR = "Back Right"
    NA = "Not Available"

class CapRockError(Exception):
    pass

def init_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    start_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    logging.basicConfig(filename='logs/%s.log' % start_time,level=logging.DEBUG)

def load_storage():
    """
    Returns tuple of previus stored data
    (Users, Drinks, Liquids)
    """
    if not os.path.exists('backend'):
        raise FileNotFoundError("Backend directory not available")
    return ([], [], [])
    #return (load_user_info(), load_drink_info(), load_liquid_info())

def save_storage(users, drinks, liquids):
    """ Saves information to storage """

    if not os.path.exists('backend'):
        os.mkdir('backend')
    try:
       # save_user_info()
        save_drink_info(drinks)
        #save_liquid_info()
    except Exception as e:
        logging.error("%s : Failed to save user info!" % str(e))



def save_drink_info(drinks):
    try:
        with open("backend/drink_storage.txt", "w") as f:
            for drink in drinks:
                f.write("%s\n" % drink.get_name())
                f.write("%f\n" % drink.get_abv())
                for liq in drink.get_liquids():
                    f.write("%s-%f\n" % (liq[0], liq[1]))
                f.write("%f" % drink.get_volume())
                f.write("\n-----\n")
            logging.info("Saved current drink storage!")
    except Exception as e:
        logging.error("%s : Failed to save drink storage!" % str(e))
        raise CapRockError("drink_storage.txt failed to save!")


def load_drink_info():
    """ Loads previous drink info from storage """
    pass