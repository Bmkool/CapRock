"""
CapRock_main.py - Main program to run the CapRock software
@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 4/10/2020
"""

import CapRock_liquid as liquid
import CapRock_drink as drink
import CapRock_user as user
import CapRock_backend_util as util
import CapRock_gui_frames as gui
import logging

def startup():
    """ Initial routine to setup software """
    try:
        util.init_logging()
        return util.load_storage()
    except Exception as e:
        logging.critical("%s - Startup issue" % str(e))
        return [], [], []


def cleanup():
    """ Cleanup actions to exit software """
    pass



# Full main Program
if __name__ == "__main__":

    # Load Previous Information from storage
    profiles, drinks, liquids = startup()
    app = gui.CapRockGUI(profiles, drinks, liquids)
    app.mainloop() # Run GUI
    cleanup()
