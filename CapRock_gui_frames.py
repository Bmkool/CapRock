"""
CapRock_gui_frames.py - Class to hold all the GUI frames

@author: Brian Kachala - ECE 4900 Team 8
@Last Edited: 4/10/2020
"""
import tkinter as tk
from tkinter import font  as tkfont
from datetime import datetime
import CapRock_backend_util as util
import CapRock_user as user
import CapRock_liquid as liquid
import CapRock_drink as drink

DARK_GRAY = "#A9A9A9"
LIME = "#00FF00"
ORANGE = "#FFA500"
CYAN = "#00FFFF"
GUEST = 9

class CapRockGUI(tk.Tk):
    """
    Runs the CapRock GUI
    """

    def __init__(self, profiles, drinks, liquids):
        tk.Tk.__init__(self)
        self.profiles = profiles
        self.drinks = drinks
        self.liquids = liquids
        self._active_profile = user.User("Guest", util.Sex.Male, 160, util.Experience.Regular) if (not profiles) else profiles[0]
        self._stored_liquids = util.current_liquids(self.liquids) # {container_code_str:liquid_obj}
        self._display_message = tk.StringVar()
        self._prev_frame = "MainMenu"
        self._delete_list = []

        #self.geometry("1000x700")
        self.attributes('-fullscreen', True) # Set Fullscreen


        self.title_font = tkfont.Font(family='Verdana', size=24, weight="bold")
        self.task_font = tkfont.Font(family='Verdana', size=12)
        self.label_font = tkfont.Font(family='Verdana', size=18)
        self.scroll_font = tkfont.Font(family='Verdana', size=14)

        tb = TaskBar(self)
        tb.pack(side="top")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)

        container.pack(side="top")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["MainMenu"] = MainMenu(parent=container, controller=self)
        self.frames["PourDrink"] = PourDrink(parent=container, controller=self)
        self.frames["ChangeProfile"] = ChangeProfile(parent=container, controller=self)
        self.frames["NewProfile"] = NewProfile(parent=container, controller=self)
        self.frames["EditProfile"] = EditProfile(parent=container, controller=self)
        self.frames["EditLiquids"] = EditLiquids(parent=container, controller=self)
        self.frames["NewLiquid"] = NewLiquid(parent=container, controller=self)
        self.frames["EditDrinks"] = EditDrinks(parent=container, controller=self)
        self.frames["NewDrink"] = NewDrink(parent=container, controller=self)
        self.frames["DeleteOption"] = DeleteOption(parent=container, controller=self)
        self.frames["DisplayInfo"] = DisplayInfo(parent=container, controller=self)

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        self.frames["MainMenu"].grid(row=0, column=0, sticky="nsew")
        self.frames["PourDrink"].grid(row=0, column=0, sticky="nsew")
        self.frames["ChangeProfile"].grid(row=0, column=0, sticky="nsew")
        self.frames["NewProfile"].grid(row=0, column=0, sticky="nsew")
        self.frames["EditProfile"].grid(row=0, column=0, sticky="nsew")
        self.frames["EditLiquids"].grid(row=0, column=0, sticky="nsew")
        self.frames["NewLiquid"].grid(row=0, column=0, sticky="nsew")
        self.frames["EditDrinks"].grid(row=0, column=0, sticky="nsew")
        self.frames["NewDrink"].grid(row=0, column=0, sticky="nsew")
        self.frames["DeleteOption"].grid(row=0, column=0, sticky="nsew")
        self.frames["DisplayInfo"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

        self.after(60000, self.save_state)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def save_state(self):
        """ Saves all profile, drink, and liquid information to storage every minute """
        util.save_storage(self.profiles, self.drinks, self.liquids)
        self.after(60000, self.save_state)

class TaskBar(tk.Frame):
    """ Set of widgets in taskbar that is shown on every frame """
    def __init__(self, controller):

        tk.Frame.__init__(self)
        self.controller = controller

        # Define Widgets
        self.profileName = tk.Label(self, text=controller._active_profile.get_name(), font=controller.task_font, width=util.NAME_MAX_LEN+1, bd=1, relief="raised")
        self.profileBAC = tk.Label(self, text="BAC: %.2f%%" % controller._active_profile.get_bac(), font=controller.task_font, width=11, bd=1, relief="raised")
        changeProfile = tk.Button(self, text="Change Profile", command=lambda: controller.show_frame("ChangeProfile"), font=controller.task_font, bd=1, highlightthickness=0)
        editDrinks = tk.Button(self, text="Edit Drinks", command=lambda: controller.show_frame("EditDrinks"), font=controller.task_font, bd=1, highlightthickness=0)
        editLiquids = tk.Button(self, text="Edit Liquids", command=lambda: controller.show_frame("EditLiquids"), font=controller.task_font, bd=1, highlightthickness=0)
        self.displayTime = tk.Label(self, text=datetime.now().strftime("%I:%M %p"), font=controller.task_font, width=9, bd=1, relief="raised")
        backToMenu = tk.Button(self, text="To Menu", command=lambda: controller.show_frame("MainMenu"), font=controller.task_font, bd=1, highlightthickness=0)
        # Layout Widgets
        self.profileName.grid(column=0, row=0, sticky="nsew")
        self.profileBAC.grid(column=1, row=0, sticky="nsew")
        changeProfile.grid(column=2, row=0, sticky="nsew")
        editDrinks.grid(column=3, row=0, sticky="nsew")
        editLiquids.grid(column=4, row=0, sticky="nsew")
        self.displayTime.grid(column=5, row=0, sticky="nsew")
        backToMenu.grid(column=6, row=0, sticky="nsew")
        self.after(1000, self.refresh)


    def refresh(self):
        """ Redraws Task Bar every second """
        self.profileName.configure(text=self.controller._active_profile.get_name())
        self.profileBAC.configure(text="BAC: %.2f%%" % self.controller._active_profile.get_bac())
        self.displayTime.configure(text=datetime.now().strftime("%I:%M %p"))
        self.after(1000, self.refresh)

class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        label = tk.Label(self, text="CapRock Automated Bartender", font=controller.title_font, pady=40)
        pourButton = tk.Button(self, text="Pour a drink!", bg=DARK_GRAY, activebackground=DARK_GRAY, font=tkfont.Font(family='Verdana', size=20, weight="bold"), width=25, height=6,
                            command=lambda: controller.show_frame("PourDrink"))
        turnOff = tk.Button(self, text="Power Off", command=lambda: self.power_off(), bg="red", activebackground="red", font=controller.label_font, bd=1, pady=10)
        pad = tk.Label(self)

        # Layout Widgets
        self.grid_columnconfigure(0,minsize=800)
        label.grid(row=0)
        pourButton.grid(row=2)
        pad.grid(row=3, ipady=20)
        turnOff.grid(row=4, ipadx=3)

    def power_off(self):
        """ Save sate and exit GUI """
        util.save_storage(self.controller.profiles, self.controller.drinks, self.controller.liquids)
        self.controller.destroy()

class PourDrink(tk.Frame):

    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        drinkLabel = tk.Label(self, text="Select a Drink: ", font=controller.label_font)
        """ Scroll Box of Drinks """
        drinkScroll = tk.Scrollbar(self)
        self.drinkChoice = tk.Listbox(self, yscrollcommand=drinkScroll.set, selectmode=tk.SINGLE)
        for dr in self.controller.drinks:
            self.drinkChoice.insert(tk.END, dr.get_name())
        drinkScroll.config(command=self.drinkChoice.yview)
        self.drinkChoice.config(font=controller.scroll_font)

        selectButton = tk.Button(self, text="Select Drink", command=lambda: self.select_drink(self.drinkChoice.curselection()), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=10)
        pad = tk.Label(self)

        # Layout Widgets
        self.grid_columnconfigure(0, minsize=250)
        self.grid_columnconfigure(1, minsize=300)
        self.grid_columnconfigure(2, minsize=800-250-300)
        self.grid_rowconfigure(0, minsize=100)

        pad.grid(row=0)
        drinkLabel.grid(row=1, column=0, sticky="e")
        self.drinkChoice.grid(row=1, column=1, sticky="ew")
        drinkScroll.grid(row=1, column=2, sticky="wns")
        selectButton.grid(row=2, column=1, pady=5)

        self.after(500, self.refresh)

    def refresh(self):
        """ Checks for drinks update every half second """
        update = False

        for dr in self.controller.drinks:
            if dr.get_name() not in self.drinkChoice.get(0, tk.END):
                update = True
                break

        for dr in self.drinkChoice.get(0,tk.END):
            if dr not in [temp.get_name() for temp in self.controller.drinks]:
                update = True
                break

        # Delete and add back valid choices
        if update:
            self.drinkChoice.delete(0, tk.END)
            for dr in self.controller.drinks:
                self.drinkChoice.insert(tk.END,dr.get_name())

        self.after(500, self.refresh)

    def select_drink(self, choice):
        if choice: # If no option then ignore click
            idx = choice[0]
            liq_id = -1
            errorMsg = ""

            # Check to make sure all liquids are currently in drink and enough volume available
            for liq in self.controller.drinks[idx].get_liquids_obj():
                name = liq[drink.LIQUID_POS].get_name()
                volume = liq[drink.VOLUME_POS]
                if name not in [("" if key is None else key.get_name()) for key in self.controller._stored_liquids.values()]:
                    errorMsg = "Unable to make %s! %s is not in storage." % (self.controller.drinks[idx].get_name(), name)

                else:
                    liq_id = util.findId(self.controller.liquids, name)
                    if volume > self.controller.liquids[liq_id].get_volume_left():
                        errorMsg = "Unable to make %s! %s requires %s oz of liquid but only %s oz remaining" % (self.controller.drinks[idx].get_name(), name, volume, self.controller.liquids[liq_id].get_volume_left())

            if not errorMsg:
                # Drink is ready to make so update backend
                for liq in self.controller.drinks[idx].get_liquids_obj(): #Update volume of liquiuds used to make drink
                    liq_id = util.findId(self.controller.liquids, liq[drink.LIQUID_POS].get_name())
                    self.controller.liquids[liq_id].change_volume_left(self.controller.liquids[liq_id].get_volume_left()-liq[drink.VOLUME_POS])

                self.controller._display_message.set("Pouring your %s. Enjoy!" % self.controller.drinks[idx].get_name())
                self.controller._active_profile.add_drink(self.controller.drinks[idx])
            else:
                self.controller._display_message.set(errorMsg)

            # Send to display screen - Wait for update
            self.controller._prev_frame = "PourDrink"
            self.controller.show_frame("DisplayInfo")

class ChangeProfile(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.choice = tk.IntVar()
        # Define Widgits:
        profilesLabel = tk.Label(self, text="Select a Profile:", font=controller.label_font)
        i = 0
        self.buttons = [] # [radiobutton, prof_name_str]

        for i in range(8):
            prof = None
            if i < len(self.controller.profiles):
                prof = self.controller.profiles[i]
            else:
                prof = user.User("Default %d" % i, util.Sex.Male, 0, util.Experience.Light)
            self.buttons.append([tk.Radiobutton(self, text=prof.get_name(), variable=self.choice, value = i, font=self.controller.scroll_font, state=(tk.DISABLED if ("Default %d" % i in prof.get_name()) else tk.NORMAL)), prof.get_name()])
            i = i+1

        self.buttons.append([tk.Radiobutton(self, text="Guest", variable=self.choice, value=GUEST, font=self.controller.scroll_font), "Guest"])
        deleteProfile = tk.Button(self, text="Delete a Profile", command=lambda: self.toDelete(), bg='red', activebackground='red', font=controller.label_font, bd=1, pady=10)
        createNewProfile = tk.Button(self, text="Create New Profile", command=lambda: self.newProfile(), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=10)
        switchToProfile = tk.Button(self, text="Set as Active Profile", command=lambda: self.changeCurrentProfile(self.choice), bg=CYAN, activebackground=CYAN, font=controller.label_font, bd=1, pady=10)
        editProfile = tk.Button(self, text="Edit Active Profile", command=lambda: self.editActiveProfile(), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=10)

        # Layout Widgets
        self.grid_columnconfigure(0, minsize=400)
        profilesLabel.grid(row=0)
        for i in range(9):
            self.buttons[i][0].grid(row=i+1, sticky="w") # Layout done here
        deleteProfile.grid(row=1, column=1, rowspan=2, sticky="ew")
        createNewProfile.grid(row=3, column=1, rowspan=2, sticky="ew")
        switchToProfile.grid(row=5, column=1, rowspan=2, sticky="ew")
        editProfile.grid(row=7, column=1, rowspan=2, sticky="ew")

        self.after(500, self.refresh)

    #TODO: I was half asleep writing this who knows if it truly works
    def refresh(self):
        """ If any differences found in the lists it deletes and readds to profile """
        update = False
        for button in self.buttons:
            if button[1] not in [prof.get_name() for prof in self.controller.profiles] and not "Default" in button[1] and not "Guest" in button[1]:
                update = True

        for prof in self.controller.profiles:
            if not any(prof.get_name() in sublist for sublist in self.buttons):
                update = True

        if update:
            for i in range(8):
                prof = None
                if i < len(self.controller.profiles):
                    prof = self.controller.profiles[i]
                else:
                    prof = user.User("Default %d" % i, util.Sex.Male, 0, util.Experience.Light)
                (self.buttons[i][0]).config(text=prof.get_name(), state=(tk.DISABLED if ("Default %d" % i in prof.get_name()) else tk.NORMAL))
                self.buttons[i][1] = prof.get_name() # Change assiciated string
                i = i+1

        self.after(500, self.refresh)


    def toDelete(self):
        self.controller._delete_list = self.controller.profiles
        self.controller._prev_frame = "ChangeProfile"
        self.controller.show_frame("DeleteOption")

    def newProfile(self):
        self.controller._prev_frame = "NewProfile"
        if len(self.controller.profiles) >= util.MAX_USERS:
            self.controller._display_message.set("Max user profiles Reached! Delete a profile first to create a new profile.")
            self.controller.show_frame("DisplayInfo")
        else:
            self.controller.show_frame("NewProfile")

    def changeCurrentProfile(self, choice):
        idx = choice.get()
        # Deal with guest profile
        if idx == GUEST:
            if self.controller._active_profile.get_name() != "Guest":
                self.controller._active_profile = user.User("Guest", util.Sex.Male, 160, util.Experience.Regular)
                self.controller._display_message.set("Active profile set as Guest! BAC estimates may be significantly off and drink history won't be saved after switching accounts!")
            else:
                self.controller._display_message.set("Active profile is already Guest!")
        # Already Active Profile
        elif self.controller._active_profile.get_name() == self.controller.profiles[idx].get_name():
            self.controller._display_message.set("%s is already the active profile!" % self.controller._active_profile.get_name())
        else:
            self.controller._active_profile = self.controller.profiles[idx]
            self.controller._display_message.set("%s is set to the active profile!" % self.controller._active_profile.get_name())
        self.controller._prev_frame = "ChangeProfile"
        self.controller.show_frame("DisplayInfo")

    def editActiveProfile(self):
        self.controller._prev_frame = "EditProfile"
        # Deal with guest profile
        if "Guest" in self.controller._active_profile.get_name():
            self.controller._display_message.set("Cannot edit Guest Profile!")
            self.controller.show_frame("DisplayInfo")
        else:
            self.controller.show_frame("EditProfile")

class NewProfile(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        sexChoice = tk.IntVar()
        expChoice = tk.IntVar()
        nameLabel = tk.Label(self, text="Enter Name [%d Max Char]: " % util.NAME_MAX_LEN, font=controller.label_font)
        self.nameInput = tk.Entry(self)
        weightLabel= tk.Label(self, text="Enter Weight [lbs]: ", font=controller.label_font)
        self.weightInput = tk.Entry(self)
        sexLabel = tk.Label(self, text="Select Sex: ", font=controller.label_font)
        self.maleRb = tk.Radiobutton(self, text="Male", variable=sexChoice, value=0, font=self.controller.scroll_font)
        self.femaleRb = tk.Radiobutton(self, text="Female",variable=sexChoice, value=1, font=self.controller.scroll_font)
        expLabel= tk.Label(self, text="Select Alcohol Experience: ", font=controller.label_font)
        self.lightRb = tk.Radiobutton(self, text="Light [<5/per Month]", variable=expChoice, value=0, font=self.controller.scroll_font)
        self.regRb = tk.Radiobutton(self, text="Regular",variable=expChoice, value=1, font=self.controller.scroll_font)
        self.heavyRb = tk.Radiobutton(self, text="Heavy [>60/per Month]", variable=expChoice, value=2, font=self.controller.scroll_font)
        createButton = tk.Button(self, text="Create Profile", command=lambda: self.createProfile(sexChoice, expChoice), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=10)
        back = tk.Button(self, text="Back", command=lambda: controller.show_frame("ChangeProfile"), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=10, padx=30)


        # Layout Widgets
        self.controller.grid_columnconfigure(0, minsize=300)
        nameLabel.grid(row=0, column=0, sticky="w")
        self.nameInput.grid(row=0, column=1, sticky="w")
        weightLabel.grid(row=1, column=0, sticky="w")
        self.weightInput.grid(row=1, column=1, sticky="w")
        sexLabel.grid(row=2, column=0, sticky="w")
        self.maleRb.grid(row=2, column=1, sticky="w")
        self.femaleRb.grid(row=3, column=1, sticky="w")
        expLabel.grid(row=4, column=0, sticky="w")
        self.lightRb.grid(row=4, column=1, sticky="w")
        self.regRb.grid(row=5, column=1, sticky="w")
        self.heavyRb.grid(row=6, column=1, sticky="w")
        createButton.grid(row=7)
        back.grid(row=7, column=1)

    def createProfile(self, sexChoice, expChoice):
        dispMessage = ""
        if not sexChoice or not expChoice: # Must have a choice for both
            return
        if len(self.nameInput.get()) > util.NAME_MAX_LEN or not self.nameInput.get():
            dispMessage = "Name must be between 1 and 12 characters!"
        if self.nameInput.get() in [subset.get_name() for subset in self.controller.profiles] or self.nameInput.get().lower() == "guest":
            dispMessage = "Cannot of multiple profiles with the same name!"
        if not self.weightInput.get().isdigit():
            dispMessage = "Weight must be a number!"
        if not dispMessage:
            # Profile is ready to add so update backend
            sex = util.Sex.Male if sexChoice == 0 else util.Sex.Female
            exp = util.Experience.Light
            if expChoice == 1:
                exp = util.Experience.Regular
            elif expChoice == 2:
                exp = util.Experience.Heavy
            self.controller.profiles.append(user.User(self.nameInput.get(), sex, float(self.weightInput.get()), exp))
            dispMessage = "Profile Successfully Added!"
            self.controller._prev_frame = "ChangeProfile"

        self.controller._display_message.set(dispMessage)
        self.controller.show_frame("DisplayInfo")

class EditProfile(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        sexChoice = tk.IntVar()
        expChoice = tk.IntVar()
        self.nameLabel = tk.Label(self, text="Editing %s's Profile" % self.controller._active_profile.get_name(), font=controller.label_font)
        weightLabel= tk.Label(self, text="Enter Weight [lbs]: ", font=controller.label_font)
        self.weightInput = tk.Entry(self)
        sexLabel = tk.Label(self, text="Select Sex: ", font=controller.label_font)
        self.maleRb = tk.Radiobutton(self, text="Male", variable=sexChoice, value=0, font=self.controller.scroll_font)
        self.femaleRb = tk.Radiobutton(self, text="Female",variable=sexChoice, value=1, font=self.controller.scroll_font)
        expLabel= tk.Label(self, text="Select Alcohol Experience: ", font=controller.label_font)
        self.lightRb = tk.Radiobutton(self, text="Light [<5/per Month]", variable=expChoice, value=0, font=self.controller.scroll_font)
        self.regRb = tk.Radiobutton(self, text="Regular",variable=expChoice, value=1, font=self.controller.scroll_font)
        self.heavyRb = tk.Radiobutton(self, text="Heavy [>60/per Month]", variable=expChoice, value=2, font=self.controller.scroll_font)
        createButton = tk.Button(self, text="Confirm Edits", command=lambda: self.editProfile(sexChoice, expChoice), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=10)
        back = tk.Button(self, text="Back", command=lambda: controller.show_frame("ChangeProfile"), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=10, padx=30)


        # Layout Widgets
        self.controller.grid_columnconfigure(0, minsize=300)
        self.nameLabel.grid(row=0, column=0, sticky="w")
        weightLabel.grid(row=1, column=0, sticky="w")
        self.weightInput.grid(row=1, column=1, sticky="w")
        sexLabel.grid(row=2, column=0, sticky="w")
        self.maleRb.grid(row=2, column=1, sticky="w")
        self.femaleRb.grid(row=3, column=1, sticky="w")
        expLabel.grid(row=4, column=0, sticky="w")
        self.lightRb.grid(row=4, column=1, sticky="w")
        self.regRb.grid(row=5, column=1, sticky="w")
        self.heavyRb.grid(row=6, column=1, sticky="w")
        createButton.grid(row=7)
        back.grid(row=7, column=1)
        self.after(1000, self.refresh)

    def refresh(self):
        """ Checks for different active profile every second """
        self.nameLabel.config(text="Editing %s's Profile" % self.controller._active_profile.get_name())
        self.after(1000, self.refresh)

    def editProfile(self, sexChoice, expChoice):
        dispMessage = ""
        if not sexChoice or not expChoice: # Must have a choice for both
            return
        if not self.weightInput.get().isdigit():
            dispMessage = "Weight must be a number!"
        if not dispMessage:
            # Profile is ready to add so update backend
            sex = util.Sex.Male if sexChoice == 0 else util.Sex.Female
            exp = util.Experience.Light
            if expChoice == 1:
                exp = util.Experience.Regular
            elif expChoice == 2:
                exp = util.Experience.Heavy
            self.controller._active_profile.change_weight(self.weightInput.get())
            self.controller._active_profile.change_sex(sex)
            self.controller._active_profile.change_experience(exp)
            self.controller._display_message.set("Profile Successfully Edited!")
        else:
            self.controller._prev_frame = "ChangeProfile"
            self.controller._display_message.set(dispMessage)
        self.controller.show_frame("DisplayInfo")

class EditDrinks(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        drinkLabel = tk.Label(self, text="Current Drinks", font=controller.label_font)
        """ Scroll Box of Drinks """
        drinkScroll = tk.Scrollbar(self)
        self.drinkChoice = tk.Listbox(self, yscrollcommand=drinkScroll.set, selectmode=tk.SINGLE)
        for dr in self.controller.drinks:
            self.drinkChoice.insert(tk.END, dr.get_name())
        drinkScroll.config(command=self.drinkChoice.yview)
        self.drinkChoice.config(font=controller.scroll_font)

        newDrink = tk.Button(self, text="Add New Drink", command=lambda: self.add_drink(), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=10)
        deleteDrink = tk.Button(self, text="Delete a Drink", command=lambda: self.delete_drink(), bg='red', activebackground='red', font=controller.label_font, bd=1, pady=10)
        viewDrink = tk.Button(self, text="View Selected Drink", command=lambda: self.view_drink(self.drinkChoice.curselection()), bg=CYAN, activebackground=CYAN, font=controller.label_font, bd=1, pady=10)
        pad = tk.Label(self)

        # Layout Widgets
        self.grid_columnconfigure(0, minsize=50)
        self.grid_columnconfigure(1, minsize=300)
        self.grid_columnconfigure(2, minsize=100)
        self.grid_rowconfigure(0, minsize=100)

        pad.grid(row=0, column=0)

        drinkLabel.grid(row=0, column=1)
        self.drinkChoice.grid(row=1, rowspan=3,  column=1, sticky="ew")
        drinkScroll.grid(row=1, rowspan=3, column=2, sticky="wns")
        newDrink.grid(row=1, column=3)
        deleteDrink.grid(row=2, column=3)
        viewDrink.grid(row=3, column=3)
        self.after(500, self.refresh)


    def refresh(self):
        """ Checks for drinks update every half second """
        update = False

        for dr in self.controller.drinks:
            if dr.get_name() not in self.drinkChoice.get(0, tk.END):
                update = True
                break

        for dr in self.drinkChoice.get(0,tk.END):
            if dr not in [temp.get_name() for temp in self.controller.drinks]:
                update = True
                break

        # Delete and add back valid choices
        if update:
            self.drinkChoice.delete(0, tk.END)
            for dr in self.controller.drinks:
                self.drinkChoice.insert(tk.END,dr.get_name())

        self.after(500, self.refresh)

    def add_drink(self):
        self.controller._prev_frame = "EditDrinks"
        if len(self.controller.drinks) > util.MAX_DRINKS_STORED:
            self.controller._display_message.set("Max drink storage Reached! Delete a drink first to create a new one.")
            self.controller.show_frame("DisplayInfo")
        else:
            self.controller.show_frame("NewDrink")

    def delete_drink(self):
        self.controller._delete_list = self.controller.drinks
        self.controller._prev_frame = "EditDrinks"
        self.controller.show_frame("DeleteOption")

    def view_drink(self, choice):
        self.controller._prev_frame = "EditDrinks"
        if choice:
            info = self.controller.drinks[choice[0]].get_liquids_name()
            toPrint = "Name: %s\nABV: %.2f%%\n\n" % (self.controller.drinks[choice[0]].get_name(), self.controller.drinks[choice[0]].get_abv()*100)
            for liq in info:
                toPrint = toPrint + str(liq[1]) + " oz of " + liq[0] + "\n"
            self.controller._display_message.set(toPrint)
            self.controller.show_frame("DisplayInfo")

class NewDrink(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        nameLabel = tk.Label(self, text="Enter Name [%d Max Char]: " % util.DRINK_MAX_LEN, font=controller.label_font)
        self.nameInput = tk.Entry(self, width=24)
        liqLabel =  []
        volLabel =  []
        self.volEntry = []
        drinkScroll = []
        self.drinkChoice = []
        """ Scroll Box of Drinks """
        for i in range(4):
            liqLabel.append(tk.Label(self, text="Liquid %d:" % (i+1), font=controller.label_font))
            volLabel.append(tk.Label(self, text="Amount [oz]:", font=controller.label_font))
            drinkScroll.append(tk.Scrollbar(self))
            self.drinkChoice.append(tk.Listbox(self, yscrollcommand=drinkScroll[i].set, selectmode=tk.SINGLE, exportselection=0, height=1, width=24))
            self.drinkChoice[i].insert(tk.END, "") # Blank
            for dr in self.controller.liquids:
                self.drinkChoice[i].insert(tk.END, dr.get_name())
            drinkScroll[i].config(command=self.drinkChoice[i].yview)
            self.drinkChoice[i].config(font=controller.scroll_font)
            self.drinkChoice[i].select_set(0)

            # Spinbox for volumes
            self.volEntry.append(tk.Spinbox(self, from_=.5, to=16, increment=.5, width=5))
            self.volEntry[i].delete(0,tk.END) # Delete text in spinbox

        createButton = tk.Button(self, text="Create Drink", command=lambda: self.createDrink(), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=10)
        back = tk.Button(self, text="Back", command=lambda: controller.show_frame("EditDrinks"), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=10, padx=30)

        # Layout Widgets
        self.grid_columnconfigure(0, minsize=300)
        self.grid_columnconfigure(1, minsize=30)
        self.grid_columnconfigure(2, minsize=800-30-300)

        nameLabel.grid(row=0, column=0, pady=20)
        self.nameInput.grid(row=0, column=1, columnspan=2, sticky="w")
        for i in range(1,5):
            liqLabel[i-1].grid(row=i*2, column=0, pady=5)
            volLabel[i-1].grid(row=i*2, column=2)
            self.drinkChoice[i-1].grid(row=i*2+1, column=0, sticky="e")
            drinkScroll[i-1].grid(row=i*2+1, column=1, sticky="w")
            self.volEntry[i-1].grid(row=i*2+1, column=2)
        createButton.grid(row=10, column=0, pady=10)
        back.grid(row=10, column=2, pady=10)
        self.after(1000, self.refresh)

    def refresh(self):
        update = False
        for i in range(4):
            for dr in self.controller.liquids:
                if dr.get_name() not in self.drinkChoice[i].get(0, tk.END):
                    update = True
                    break

            for dr in self.drinkChoice[i].get(0,tk.END):
                if dr and dr not in [temp.get_name() for temp in self.controller.liquids]:
                    update = True
                    break

            # Delete and add back valid choices
            if update:
                self.drinkChoice[i].delete(0, tk.END)
                self.drinkChoice[i].insert(tk.END, "") # Blank
                for dr in self.controller.liquids:
                    self.drinkChoice[i].insert(tk.END,dr.get_name())
                self.drinkChoice[i].select_set(0)

        self.after(1000, self.refresh)


    def createDrink(self):
        drinkName = self.nameInput.get()
        dispMessage = ""
        self.controller._prev_frame = "NewDrink"
        if len(drinkName) > util.DRINK_MAX_LEN or not drinkName:
            dispMessage = "Name must be between 1 and %d characters!" % util.DRINK_MAX_LEN
        elif drinkName in [subset.get_name() for subset in self.controller.drinks]:
            dispMessage = "Drink with same name already exists!"
        else:
            goodLiq = []
            for i in range(4):
                liqNum = self.drinkChoice[i].curselection()[0]
                volTemp = self.volEntry[i].get()
                if liqNum > 0: # Liquid should be added
                    if not volTemp.replace('.','',1).isdigit():
                        dispMessage = "Volume must be a number"
                        break
                    else:
                        volNum = float(volTemp)
                        if volNum not in [x*0.5 for x in range(2*0, 2*16+1)][1:]: # Make sure in range .5-16
                            dispMessage = "Volume must be in increments of .5 oz from .5-16"
                        else:
                            goodLiq.append((self.controller.liquids[liqNum-1],volNum)) # Add liquid to drink

            # Add drink to list
            if goodLiq:
                self.makeDrink(drinkName, goodLiq)
                dispMessage = "%s added to drink list!" % drinkName
                self.controller._prev_frame = "EditDrinks"
            elif not dispMessage:
                dispMessage = "No liquids selected! Be sure to click on box to turn background gray to confirm liquid selection."

        # Display results
        self.controller._display_message.set(dispMessage)
        self.controller.show_frame("DisplayInfo")

    def makeDrink(self, drinkName, goodLiq):
        if len(goodLiq) == 1:
            self.controller.drinks.append(drink.Drink(drinkName, goodLiq[0]))
        elif len(goodLiq) == 2:
            self.controller.drinks.append(drink.Drink(drinkName, goodLiq[0], goodLiq[1]))
        elif len(goodLiq) == 3:
            self.controller.drinks.append(drink.Drink(drinkName, goodLiq[0], goodLiq[1], goodLiq[2]))
        else:
            self.controller.drinks.append(drink.Drink(drinkName, goodLiq[0], goodLiq[1], goodLiq[2], goodLiq[3]))

class EditLiquids(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._containers = {0:util.Container.FL, 1:util.Container.FR, 2:util.Container.BL, 3:util.Container.BR}

        # Define Widgets
        liquidLabel = tk.Label(self, text="Choose Liquid", font=controller.label_font)
        containerLabel = tk.Label(self, text="Choose Container", font=controller.label_font)
        curLiquidLabel = tk.Label(self, text="Current Liquids", font=controller.label_font)
        volLabel = tk.Label(self, text="Set Volume", font=controller.label_font)

        """ Scroll Box of Liquids """
        liquidScroll = tk.Scrollbar(self)
        self.liquidChoice = tk.Listbox(self, yscrollcommand=liquidScroll.set, exportselection=0, selectmode=tk.SINGLE, height=5)
        for dr in self.controller.liquids:
            self.liquidChoice.insert(tk.END, dr.get_name())
        self.liquidChoice.insert(tk.END, "No Liquid")
        liquidScroll.config(command=self.liquidChoice.yview)
        self.liquidChoice.config(font=controller.scroll_font)

        """ Scroll Box of Containers """
        containerScroll = tk.Scrollbar(self)
        self.containerChoice = tk.Listbox(self, yscrollcommand=containerScroll.set, exportselection=0, selectmode=tk.SINGLE, height=5)
        for dr in ("Front Left - FL", "Front Right - FR", "Back Left - BL", "Back Right - BR"):
            self.containerChoice.insert(tk.END, dr)
        containerScroll.config(command=self.containerChoice.yview)
        self.containerChoice.config(font=controller.scroll_font)


        self.volEntry = tk.Spinbox(self, from_=.5, to=16, increment=.5, width=5)
        self.volEntry.delete(0,tk.END) # Delete text in spinbox

        newLiquid = tk.Button(self, text="Add New Liquid", command=lambda: self.addLiquid(), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=5)
        confirmChange = tk.Button(self, text="Confirm Change", command=lambda: self.changeLiquid(), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=5)
        deleteLiquid = tk.Button(self, text="Delete Liquid", command=lambda: self.delete_liquid(), bg='red', activebackground='red', font=controller.label_font, bd=1, pady=5)
        viewLiquid = tk.Button(self, text="View Liquid", command=lambda: self.view_liquid(self.liquidChoice.curselection()), bg=CYAN, activebackground=CYAN, font=controller.label_font, bd=1, pady=5)

        self.FLText = tk.StringVar()
        self.FRText = tk.StringVar()
        self.BLText = tk.StringVar()
        self.BRText = tk.StringVar()
        self.updateContainerText()
        self.FLBox = tk.Message(self, textvariable=self.FLText, font=controller.task_font, bd=1, relief="raised", width=120, anchor=tk.NW)
        self.FRBox = tk.Message(self, textvariable=self.FRText, font=controller.task_font, bd=1, relief="raised", width=120, anchor=tk.NW)
        self.BLBox = tk.Message(self, textvariable=self.BLText, font=controller.task_font, bd=1, relief="raised", width=120, anchor=tk.NW)
        self.BRBox = tk.Message(self, textvariable=self.BRText, font=controller.task_font, bd=1, relief="raised", width=120, anchor=tk.NW)

        pad = tk.Label(self)

        # Layout Widgets
        self.grid_columnconfigure(0, minsize=50)
        self.grid_columnconfigure(2, minsize=30)
        self.grid_columnconfigure(3, minsize=120)
        self.grid_columnconfigure(4, minsize=120)
        self.grid_columnconfigure(5, minsize=120)
        #self.grid_columnconfigure(2, minsize=800-30-300)

        pad.grid(row=0)
        liquidLabel.grid(row=0, column=1, pady=5)
        self.liquidChoice.grid(row=1, column=1, sticky="nse")
        liquidScroll.grid(row=1, column=2, sticky="nsw")
        containerLabel.grid(row=2, column=1)
        self.containerChoice.grid(row=3, column=1, pady=2, sticky="nse")
        containerScroll.grid(row=3, column=2, sticky="nsw")
        confirmChange.grid(row=5, column=1, pady=2)
        viewLiquid.grid(row=5, column=4, pady=2, columnspan=2)
        newLiquid.grid(row=6, column=1, pady=0, padx=10)
        deleteLiquid.grid(row=6, column=4, columnspan=3, pady=10, padx=10)
        curLiquidLabel.grid(row=0, column=4, columnspan=2)
        volLabel.grid(row=0, column=3, padx=10)
        self.volEntry.grid(row=1, column=3, sticky="n")
        self.BLBox.grid(row=1, column=4, rowspan=1, sticky="nsew")
        self.BRBox.grid(row=1, column=5, rowspan=1, sticky="nsew")
        self.FLBox.grid(row=3, column=4, rowspan=1, sticky="nsew")
        self.FRBox.grid(row=3, column=5, rowspan=1, sticky="nsew")

        self.after(1000, self.refresh)

    def refresh(self):
        self.updateContainerText()
        update = False

        for dr in self.controller.liquids:
            if dr.get_name() not in self.liquidChoice.get(0, tk.END):
                update = True
                break

        for dr in self.liquidChoice.get(0,tk.END):
            if dr not in [temp.get_name() for temp in self.controller.liquids] and dr != "No Liquid":
                update = True
                break

        # Delete and add back valid choices
        if update:
            self.liquidChoice.delete(0, tk.END)
            for dr in self.controller.liquids:
                self.liquidChoice.insert(tk.END,dr.get_name())
            self.liquidChoice.insert(tk.END,"No Liquid")

        self.after(1000, self.refresh)

    def updateContainerText(self):
        """ Updates stringvar to container with new liquid """
        fl_obj = self.controller._stored_liquids.get("FL")
        fr_obj = self.controller._stored_liquids.get("FR")
        bl_obj = self.controller._stored_liquids.get("BL")
        br_obj = self.controller._stored_liquids.get("BR")
        fl_name = fl_obj.get_name() if (fl_obj is not None) else "No Liquid"
        fl_vol = fl_obj.get_volume_left() if (fl_obj is not None) else 0
        fr_name = fr_obj.get_name() if (fr_obj is not None) else "No Liquid"
        fr_vol = fr_obj.get_volume_left() if (fr_obj is not None) else 0
        bl_name = bl_obj.get_name() if (bl_obj is not None) else "No Liquid"
        bl_vol = bl_obj.get_volume_left() if (bl_obj is not None) else 0
        br_name = br_obj.get_name() if (br_obj is not None) else "No Liquid"
        br_vol = br_obj.get_volume_left() if (br_obj is not None) else 0

        self.FLText.set("%s\n\n%s\n\n%.1f oz" % ("       F\u0332L\u0332", fl_name, fl_vol))
        self.FRText.set("%s\n\n%s\n\n%.1f oz" % ("       F\u0332R\u0332", fr_name, fr_vol))
        self.BLText.set("%s\n\n%s\n\n%.1f oz" % ("       B\u0332L\u0332", bl_name, bl_vol))
        self.BRText.set("%s\n\n%s\n\n%.1f oz" % ("       B\u0332R\u0332", br_name, br_vol))

    def addLiquid(self):
        self.controller._prev_frame = "EditLiquids"
        if len(self.controller.liquids) > util.MAX_LIQUIDS_STORED:
            self.controller._display_message.set("Max liquid storage Reached! Delete a liquid first to create a new one.")
            self.controller.show_frame("DisplayInfo")
        else:
            self.controller.show_frame("NewLiquid")

    def changeLiquid(self):
        self.controller._prev_frame = "EditLiquids"
        liq = self.liquidChoice.curselection()
        container = self.containerChoice.curselection()
        volTemp = self.volEntry.get()
        if liq and container and (liq[0] == len(self.controller.liquids) or volTemp):
            dispMessage = ""
            liq_choice = liq[0]
            con_choice = container[0]
            if  liq_choice != len(self.controller.liquids) and not volTemp.replace('.','',1).isdigit():
                dispMessage = "Volume must be a number"
            elif liq_choice != len(self.controller.liquids) and float(volTemp) not in [x*0.5 for x in range(2*0, 2*16+1)][1:]: # Make sure in range .5-16
                dispMessage = "Volume must be in increments of .5 oz from .5-16"
            else: # Volume is good change container
                # Remove old liquid info
                containerName = self._containers.get(con_choice).name
                prev_liq = self.controller._stored_liquids.get(containerName) # Gets liq obj hopefully
                if prev_liq is not None:
                    liq_id = util.findId(self.controller.liquids, prev_liq.get_name())
                    self.controller.liquids[liq_id].remove_container()

                # Update liquid to new info
                if liq_choice != len(self.controller.liquids): # Didnt Chose no liquid
                    self.controller.liquids[liq_choice].change_container(self._containers.get(con_choice))
                    self.controller.liquids[liq_choice].change_volume_left(float(volTemp))

                # Update _current storage
                self.controller._stored_liquids = util.current_liquids(self.controller.liquids)
                # update text for page
                self.updateContainerText()
                dispMessage = "Sucessfully Updated Storage Information!"
            self.controller._display_message.set(dispMessage)
            self.controller.show_frame("DisplayInfo")

    def delete_liquid(self):
        self.controller._delete_list = self.controller.liquids
        self.controller._prev_frame = "EditLiquids"
        self.controller.show_frame("DeleteOption")

    def view_liquid(self, choice):
        self.controller._prev_frame = "EditLiquids"
        if choice and choice[0] < len(self.controller.liquids): # Didnt choose no liquid
            liq = self.controller.liquids[choice[0]]
            toPrint = "Name: %s\nABV: %.2f%%\nDensity: %.2f g/mL" % (liq.get_name(), liq.get_abv()*100, liq.get_density())
            self.controller._display_message.set(toPrint)
            self.controller.show_frame("DisplayInfo")

class NewLiquid(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        nameLabel = tk.Label(self, text="Enter Name:", font=controller.label_font)
        self.nameInput = tk.Entry(self)
        abvLabel = tk.Label(self, text="Enter ABV [%]: ", font=controller.label_font)
        self.abvInput = tk.Entry(self)
        densityLabel = tk.Label(self, text="Enter Density [g/mL]: ", font=controller.label_font)
        self.densityInput = tk.Entry(self)
        createButton = tk.Button(self, text="Add Liquid", command=lambda: self.add_liquid(), bg=LIME, activebackground=LIME, font=controller.label_font, bd=1, pady=10)
        back = tk.Button(self, text="Back", command=lambda: controller.show_frame("EditLiquids"), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=10, padx=30)

        # Layout Widgets
        nameLabel.grid(row=0, column=0, pady=20)
        self.nameInput.grid(row=0, column=1)
        abvLabel.grid(row=1, column=0, pady=20)
        self.abvInput.grid(row=1, column=1)
        densityLabel.grid(row=2, column=0, pady=20)
        self.densityInput.grid(row=2, column=1)
        createButton.grid(row=3, column=0)
        back.grid(row=3, column=1)

    def add_liquid(self):
        liqName = self.nameInput.get()
        abv = self.abvInput.get()
        density = self.densityInput.get()
        dispMessage = ""
        self.controller._prev_frame = "NewLiquid"
        if len(liqName) > util.LIQUID_MAX_LEN or not liqName:
            dispMessage = "Name must be between 1 and %d characters!" % util.LIQUID_MAX_LEN
        elif liqName in [subset.get_name() for subset in self.controller.liquids]:
            dispMessage = "Liquid with same name already exists!"
        elif not abv or not abv.replace('.','',1).isdigit() or float(abv) < 0 or float(abv) > 100:
            dispMessage = "ABV must be between 0-100%!"
        elif not density or not density.replace('.','',1).isdigit():
            dispMessage = "Density must be a number!"
        else:
            self.controller.liquids.append(liquid.Liquid(liqName, float(abv)/100, float(density)))
            dispMessage = "Successfully added liquid to storage!"
            self.controller._prev_frame = "EditLiquids"
        self.controller._display_message.set(dispMessage)
        self.controller.show_frame("DisplayInfo")

class DeleteOption(tk.Frame):
    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        label = tk.Label(self, text="Select to Delete: ", font=controller.label_font, fg="red")
        """ Scroll Box of Objects """
        scroll = tk.Scrollbar(self)
        self.choice = tk.Listbox(self, yscrollcommand=scroll.set, selectmode=tk.SINGLE)
        for dr in self.controller._delete_list:
            self.choice.insert(tk.END, dr.get_name())
        scroll.config(command=self.choice.yview)
        self.choice.config(font=controller.scroll_font)
        selectButton = tk.Button(self, text="Select option", command=lambda: self.select_option(self.choice.curselection()), bg="red", activebackground="red", font=controller.label_font, bd=1, pady=10)
        back = tk.Button(self, text="Back", command=lambda: controller.show_frame(self.controller._prev_frame), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=20, padx=30)
        pad = tk.Label(self)

        # Layout Widgets
        self.grid_columnconfigure(0, minsize=250)
        self.grid_columnconfigure(1, minsize=300)
        self.grid_columnconfigure(2, minsize=800-250-300)
        self.grid_rowconfigure(0, minsize=100)

        pad.grid(row=0)
        label.grid(row=1, column=0, sticky="e")
        self.choice.grid(row=1, column=1, sticky="ew")
        scroll.grid(row=1, column=2, sticky="wns")
        selectButton.grid(row=2, column=1, pady=5)
        back.grid(row=2, column=2, pady=5)

        self.after(500, self.refresh)

    def refresh(self):
        """ If any differences found in the lists it deletes and readds to delete list """
        update = False
        for item in self.choice.get(0,tk.END):
            if item not in [key.get_name() for key in self.controller._delete_list]:
                update = True

        if self.choice.size() != len(self.controller._delete_list):
            update = True

        if update:
            self.choice.delete(0, tk.END)
            for thing in self.controller._delete_list:
                self.choice.insert(tk.END, thing.get_name())

        self.after(500, self.refresh)

    def select_option(self, choice):
        if choice: # If no option then ignore click
            idx = choice[0]
            # Cant delete active profile
            if  self.controller._delete_list == self.controller.profiles and self.controller._delete_list[idx].get_name() == self.controller._active_profile.get_name():
                self.controller._display_message.set("You cannot delete the active profile!")
            # Cant delete liquid in container
            elif self.controller._delete_list == self.controller.liquids and self.controller._delete_list[idx].get_name() in [("" if liq is None else liq.get_name()) for liq in self.controller._stored_liquids.values()]:
                self.controller._display_message.set("You cannot delete a liquid currently in a container!")
            # Cant delete liquid if in any drink
            elif self.controller._delete_list == self.controller.liquids and self.liq_in_stored_drink(self.controller._delete_list[idx].get_name()):
                self.controller._display_message.set("You cannot delete a liquid currently in a drink!")
            else: # Delete Option
                self.controller._display_message.set("%s has successfully been deleted!" % self.controller._delete_list[idx].get_name())
                self.controller._delete_list.pop(idx)
            self.controller.show_frame("DisplayInfo")

    def liq_in_stored_drink(self, liq):
        ''' Checks every dr in storage if liq in a drink '''
        for dr in self.controller.drinks:
            liqs_dr = dr.get_liquids_name()
            for each_liq in liqs_dr:
                if liq == each_liq[0]:
                    return True

        return False

class DisplayInfo(tk.Frame):

    def __init__(self, parent, controller):
        # Init Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Define Widgets
        self.message = tk.Message(self, textvariable=self.controller._display_message, font=self.controller.label_font, width=400)
        back = tk.Button(self, text="Back", command=lambda: controller.show_frame(self.controller._prev_frame), bg=ORANGE, activebackground=ORANGE, font=controller.label_font, bd=1, pady=20, padx=30)

        # Layout Widgets
        self.grid_columnconfigure(0, minsize=800)
        self.grid_rowconfigure(0, minsize=300)
        self.message.grid(row=0, column=0)
        back.grid(row=1)


if __name__ == "__main__":
    us, dr, liq = util.load_storage()
    app = CapRockGUI(us,dr,liq)
    app.mainloop()