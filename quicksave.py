# TC.exe's KH Quicksave Tool
# This script allows a user to easily move autosave.dat files around.
# Although I have thoroughly tested this, I'm by no means a professional, so use this script at your discretion.

# Requires Python 3 to run.
# Requires 1fmSaveAnywhere.lua to be installed.
# This script was built for use on Windows.

import os
import sys
import shutil

# CHANGE THESE VALUES ACCORDING TO SYSTEM PREFERENCES
loc_as = "C:\\Program Files\\Epic Games\\KH_1.5_2.5\\autosave.dat" # Path to autosave.dat
loc_store = "C:\\Users\\Kane\\Documents\\Speedrun\\KH Quicksave Tool\\Saves\\" # Quicksave directory.
sav_prefix = "QS_" # Prefix for quicksave filenames.
autosave_backup = True # True will backup autosave.dat whenever loading a save. False will skip this. Case-sentitive.
confirm_changes = True # True will ask user before deleting or overwriting. False will skip this. Case-sensitive.
 
# Return list of saves
def save_list():
    array_sav = [file for file in os.listdir(loc_store) if file.endswith('.dat')]
    return array_sav

# Get user input, then clear screen, return input.
def get_user_input(max_num):

    not_valid = False

    while True:

        # Print user input display and previous invalid input.
        print("------------")
        if not_valid == False:
            print()
        else:
            print(str(usr_input) + " is not a valid input.")
        usr_input = input(">>> ")
        print()
        
        # Test if input was a valid number.
        try:
            usr_int = int(usr_input)
            if (usr_int <= max_num) and (usr_int > -1):
                return usr_int
            else:
                not_valid = True

        except ValueError:
            not_valid = True

# Writes a save
def write_sav(sav_name):
    
    loc_copy = loc_store + sav_prefix + str(sav_name) + ".dat"
    shutil.copy(loc_as, loc_copy)
    print("Save created as \"" + sav_prefix + sav_name + ".dat\"")
    print()

# Overwrite a save
def over_sav(sav_num):

    sav_name = str(save_list()[sav_num - 1])
    loc_copy = loc_store + sav_name
    shutil.copy(loc_as, loc_copy)
    print("Save \"" + sav_name + "\" overwriten.")
    print()

# Loads a save
def load_sav(sav_num):
    
    # Get save file directory
    sav_name = save_list()[sav_num - 1]
    sav_dir = loc_store + save_list()[sav_num - 1]

    # Creates an 'autosave'.
    if (autosave_backup == True) and (sav_dir != loc_store + sav_prefix + "autosave.dat"):
        shutil.copy(loc_as, loc_store + sav_prefix + "autosave.dat")
        print("Backup created as \"" + sav_prefix + "autosave.dat\".")

    # Replaces autosave.dat with selected save
    shutil.copy(sav_dir, loc_as)
    print("Save \"" + sav_name + "\" loaded.")
    print()

# Deletes a save
def del_sav(sav_num):
    
    # Get save file directory
    sav_name = loc_store + save_list()[sav_num - 1]
    os.remove(sav_name)
    print("Save \"" + sav_name + "\" deleted.")
    print()

# Prints a numbered list of saves
def print_saves():
    
    list_sav = save_list()
    list_num = 1

    for name_file in list_sav:
            print(str(list_num) + ". " + name_file)
            list_num += 1

def user_confirm():

    if confirm_changes:
        print("------------")
        print("0. Return")
        print("1. Confirm")
        usr_input = get_user_input(1)
        if usr_input == 1:
            return True
        else:
            return False
    else:
        return True


# PROGRAM LOOOOOOP
while True:
    print("\n" * 100)
    print("----MENU----")
    print("0. Exit")
    print("1. Save")
    print("2. Load")
    print("3. Rename")
    print("4. Delete")
    usr_input = get_user_input(4)

    if usr_input == 0:
            sys.exit()

    # SAVE MENU
    elif usr_input == 1: # User selects SAVE
        while usr_input != 0:
            print("----SAVE----")
            print("0. Menu")
            print("1. Write Save")
            print("2. Overwrite Save")

            usr_input = get_user_input(2)

            # Writing a save with user input
            if usr_input == 1:
                print("------------")
                print("Enter a name for this save:")
                usr_name_input = input(">>> ")
                name_input_fix = sav_prefix + str(usr_name_input) + ".dat"
                print()
                
                # Confirming an overwrite
                if name_input_fix in save_list():
                    print("The file \"" + name_input_fix + "\" already exists, would you like to replace it?")
                    usr_conf = user_confirm()
                    if usr_conf:
                        write_sav(usr_name_input)
                    else:
                        usr_input = 1
                else:    
                    write_sav(usr_name_input)
            
            # Overwriting a save using menu number
            if usr_input == 2:
                print("Select a file to overwrite:")
                print("------------")
                print("0. Return")
                print_saves()
                usr_input = get_user_input(len(save_list()))
                if usr_input > 0:
                    print("Selected: " + save_list()[usr_input - 1])
                    print("Are you sure you would like to overwrite this save?")
                    usr_conf = user_confirm()
                    if usr_conf:
                        over_sav(usr_input)
                    else:
                        usr_input = 1


    # LOAD MENU
    elif usr_input == 2: # User selects LOAD
        while usr_input != 0:
            print("----LOAD----")
            print("0. Menu")
            print_saves()
            usr_input = get_user_input(len(save_list()))
            if usr_input != 0:
                load_sav(usr_input)

    # RENAME MENU
    elif usr_input == 3: # User selects RENAME
        while usr_input != 0:
            print("---RENAME---")
            print("0. Menu")
            print_saves()
            usr_input = get_user_input(len(save_list()))
            if usr_input != 0:
                selected_save = save_list()[usr_input - 1]
                print("Selected: " + save_list()[usr_input - 1])
                print("What would you like to rename this save?")
                print("(Do not include \"" + sav_prefix + "\" or \".dat\")")
                usr_name_input = input(">>> ")
                print
                org_sav_loc = loc_store + selected_save
                copy_sav_loc = loc_store + sav_prefix + str(usr_name_input) + ".dat"
                shutil.move(org_sav_loc, copy_sav_loc)
                print("\"" + selected_save + "\" renamed to \"" + sav_prefix + usr_name_input + ".dat\"")
                print()



    # DELETE MENU
    elif usr_input == 4: # User selects DELETE
        while usr_input != 0: 
            print("---DELETE---")
            print("0. Menu")
            print_saves()
            usr_input = get_user_input(len(save_list()))
            if usr_input != 0:
                print("Selected: " + save_list()[usr_input - 1])
                print("Are you sure you could like to delete this save?")
                usr_conf = user_confirm()
                if usr_conf:
                    del_sav(usr_input)
                else:
                    usr_input = 4
