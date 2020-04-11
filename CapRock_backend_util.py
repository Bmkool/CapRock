"""
CapRock_backed_utility  - List of all constants, enums, functions and Exceptions used in CapRock Software
@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 4/10/2020
"""
from enum import Enum
import logging
import os
from datetime import datetime
import sys

MAX_LIQ_PER_DRINK = 4
MAX_LIQUIDS_STORED = 64
MAX_DRINKS_STORED = 16
MAX_USERS = 8
MAX_VOLUME_OZ = 16
NAME_MAX_LEN = 12
DRINK_MAX_LEN = 24
LIQUID_MAX_LEN = 24
SESSION_TIME = 8 # Number of hours to store drinks
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
    """ Initialized logging module """
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

    liquids = load_liquid_info()
    drinks = load_drink_info(liquids)
    users = load_user_info(drinks)
    return users, drinks, liquids

def save_storage(users, drinks, liquids):
    """ Saves information to storage """

    if not os.path.exists('backend'):
        os.mkdir('backend')
    try:
        save_user_info(users)
        save_drink_info(drinks)
        save_liquid_info(liquids)
    except Exception as e:
        logging.error("%s : Failed to save user info!" % str(e))

def findId(obj, name):
    """ Finds index of liquid, drink, or user profile based on name """
    i = 0
    for d in obj:
        if name == d.get_name():
            return i
        i = i + 1
    # If this hits the object doesnt exist
    return -1

def load_user_info(drinks):
    """ Loads previous user info from storage """
    import CapRock_user as user
    user_list = []
    try:
        with open("backend/user_storage.txt", "r") as f:
            content = f.read()
            users = content.split("\n-----\n")
            while "" in users: # Remove ending whitespaces
                    users.remove("")
            user_num = 0
            for person in users:
                temp = person.split('\n')
                while "" in temp: # Remove ending whitespaces
                    temp.remove("")
                user_list.append(user.User(temp[0], Sex[temp[1]], float(temp[2]), Experience[temp[3]]))
                j = 0
                while j < int(temp[4]): # All remaining liquids
                    num = findId(drinks, temp[6+j*2])
                    if (num >= 0): # If drink was deleted dont add
                        user_list[user_num].add_drink(drinks[num], time=temp[5+j*2])
                    j = j + 1
                user_num = user_num + 1
        return user_list

    except Exception as e:
        logging.error("%s : Failed to load user storage!" % str(e))
        return []

def load_drink_info(liquids):
    """ Loads previous drink info from storage """
    import CapRock_drink as drink
    drink_list = []
    try:
        with open("backend/drink_storage.txt", "r") as f:
            content = f.read()
            drinks = content.split("-----\n")
            while "" in drinks: # Remove ending whitespaces
                    drinks.remove("")
            drink_num = 0
            for single in drinks:
                temp = single.split('\n')
                while "" in temp: # Remove ending whitespaces
                    temp.remove("")
                num = findId(liquids, temp[2])
                if num >= 0: # If deleted before dont worry about it
                    drink_list.append(drink.Drink(temp[0], (liquids[num], float(temp[3])))) # First Liquid
                j = 0
                while j < (int(temp[1]) - 1)  and int(temp[1]) > 0: # All remaining liquids
                    num = findId(liquids, temp[4+j*2])
                    if num >= 0: # If deleted before dont worry about it
                        drink_list[drink_num].add_liquid((liquids[num], float(temp[5+j*2])))
                    j = j + 1
                drink_num = drink_num + 1
        return drink_list

    except Exception as e:
        logging.error("%s : Failed to load drink storage!" % str(e))
        return []

def load_liquid_info():
    """ Loads previous liquid info from storage """
    import CapRock_liquid as liquid
    liquid_list = []
    try:
        with open("backend/liquid_storage.txt", "r") as f:
            content = f.read()
            liquids = content.split("\n-----\n")
            while "" in liquids: # Remove ending whitespaces
                liquids.remove("")
            for liq in liquids:
                temp = liq.split("\n")
                while "" in temp: # Remove ending whitespaces
                    temp.remove("")
                liquid_list.append(liquid.Liquid(temp[0], float(temp[1]), float(temp[2]), float(temp[3]), Container[temp[4]]))
        return liquid_list

    except Exception as e:
        logging.error("%s : Failed to load drink storage!" % str(e))
        return []

def save_user_info(users):
    """ Saves user information to 'backend/user_storage.txt' """
    try:
        with open("backend/user_storage.txt", "w") as f:
            for person in users:
                f.write("%s\n" % person.get_name())
                f.write("%s\n" % person.get_sex())
                f.write("%f\n" % person.get_weight())
                f.write("%s\n" % person.get_experience())
                f.write("%d" % len(person.get_current_drinks()))
                for d in person.get_current_drinks():
                    f.write("\n%s\n%s" % (d[0], d[1].get_name()))
                f.write("\n-----\n")
            logging.info("Saved current drink storage!")
    except Exception as e:
        logging.error("%s : Failed to save drink storage!" % str(e))
        raise CapRockError("drink_storage.txt failed to save!")

def save_drink_info(drinks):
    """ Saves drink information to 'backend/drink_storage.txt' """
    try:
        with open("backend/drink_storage.txt", "w") as f:
            for d in drinks:
                f.write("%s\n" % d.get_name())
                f.write("%d\n" % len(d.get_liquids_name()))
                for liq in d.get_liquids_name():
                    f.write("%s\n%f\n" % (liq[0], liq[1]))
                f.write("-----\n")
            logging.info("Saved current drink storage!")
    except Exception as e:
        logging.error("%s : Failed to save drink storage!" % str(e))
        raise CapRockError("drink_storage.txt failed to save!")

def save_liquid_info(liquids):
    """ Saves liquid information to 'backend/liquid_storage.txt' """
    try:
        with open("backend/liquid_storage.txt", "w") as f:
            for liq in liquids:
                f.write("%s\n" % liq.get_name())
                f.write("%f\n" % liq.get_abv())
                f.write("%f\n" % liq.get_density())
                f.write("%f\n" % liq.get_volume_left())
                f.write("%s" % liq.get_container())
                f.write("\n-----\n")
            logging.info("Saved current liquid storage!")
    except Exception as e:
        logging.error("%s : Failed to save liquid storage!" % str(e))
        raise CapRockError("liquid_storage.txt failed to save!")

def current_liquids(liquids):
    """ Returns currently loaded liquids in the mixer as a dict {container_name:liquid_name} """
    storage = {Container.FL.name:None, Container.FR.name:None, Container.BL.name:None, Container.BR.name:None}
    for liq in liquids:
        if liq.get_container() != Container.NA.name:
            storage.update({liq.get_container():liq})
    return storage