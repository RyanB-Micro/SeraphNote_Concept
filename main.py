import pygame
from tkinter import *
import threading
import screen_utils as screen_ut


# Window Settings
#----------------
WIDTH = 1490
HEIGHT = 914

stop_event = threading.Event()
screen_thread = None


bond_window = Tk()
label_entry = None


def start_screen():
    global screen_thread
    stop_event.clear()
    screen_thread.start()


def stop_screen():
    global screen_thread
    stop_event.set()
    screen_thread.join(timeout=2)


def screen_loop():
    while not stop_event.is_set():
        if screen_ut.pygame_running == False:
            screen_ut.init_screen(WIDTH, HEIGHT)

        screen_ut.screen_loop()
        # Once screen loop finished -> close thread
        stop_screen()


def change_bond_text(entry):
    if screen_ut.changeable_bond is None:
        return

    text = label_entry.get()
    screen_ut.bond_list[screen_ut.changeable_bond].text = text
    screen_ut.changeable_bond = None
    bond_window.withdraw()


def create_bond_control():
    global label_entry
    bond_num = screen_ut.changeable_bond
    bond_window.geometry("200x300")
    bond_window.protocol("WM_DELETE_WINDOW", bond_window.withdraw)
    bond_window.title("Bond Control")

    title_label = Label(bond_window, text="Bond Control Settings")
    title_label.pack()


    label_entry = Entry()

    label_entry.pack()

    start_sim_button = Button(bond_window, text="Update Label")
    start_sim_button.config(command=lambda: change_bond_text(label_entry))
    start_sim_button.place(x=50, y=50)


def detect_bond_selection():
    global label_entry
    if screen_ut.pygame_running and (screen_ut.changeable_bond is not None):
        if bond_window.state() == "withdrawn":
            label_entry.delete(0, END)
            label_entry.insert(0, screen_ut.bond_list[screen_ut.changeable_bond].text)
            bond_window.deiconify()
    # recheck window after delay
    bond_window.after(100, detect_bond_selection)


def main():
    print ("Program Running")
    start_screen()
    create_bond_control()
    bond_window.withdraw()
    detect_bond_selection()
    bond_window.mainloop()

    # bond_window.withdraw()
    # while True:
    #
    #     if screen_ut.pygame_running:
    #         if screen_ut.changeable_bond:
    #             bond_window.deiconify()






# Threads
screen_thread = threading.Thread(target=screen_loop)


if __name__ == '__main__':
    main()

