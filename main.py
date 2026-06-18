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

root_window = None
node_window = None
bond_window = None
title_label_entry = None
node_label_entry = None
bond_label_entry = None

main_title_label = None


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


def change_title_text():
    global main_title_label
    new_title = title_label_entry.get().strip()
    if not new_title:
        new_title = "SeraphNote__New_File__"

    main_title_label = "SeraphNote_" + new_title
    screen_ut.window_title = main_title_label


def change_node_text():
    if screen_ut.changeable_node is None:
        return

    text = node_label_entry.get()
    screen_ut.node_list[screen_ut.changeable_node].text = text
    screen_ut.changeable_node = None
    node_window.withdraw()


def change_bond_text():
    if screen_ut.changeable_bond is None:
        return

    text = bond_label_entry.get()
    screen_ut.bond_list[screen_ut.changeable_bond].text = text
    screen_ut.changeable_bond = None
    bond_window.withdraw()


def cancel_bond_edit():
    screen_ut.changeable_bond = None
    bond_window.withdraw()

def cancel_node_edit():
    screen_ut.changeable_node = None
    node_window.withdraw()


def create_root_control():
    global title_label_entry
    # bond_num = screen_ut.changeable_node
    root_window.geometry("200x300")
    root_window.protocol("WM_DELETE_WINDOW", root_window.withdraw)
    root_window.title("Main Control")

    title_label = Label(root_window, text="Main Control Panel")
    title_label.pack()

    title_label_entry = Entry(root_window)
    title_label_entry.pack()

    change_title_button = Button(root_window, text="Update Label")
    change_title_button.config(command=lambda: change_title_text())
    change_title_button.place(x=50, y=50)


def create_node_control():
    global node_label_entry
    node_window.geometry("200x300")
    node_window.protocol("WM_DELETE_WINDOW", cancel_node_edit)
    node_window.title("Node Control")

    title_label = Label(node_window, text="Node Control Panel")
    title_label.pack()

    node_label_entry = Entry(node_window)
    node_label_entry.pack()

    update_label_button = Button(node_window, text="Update Label")
    update_label_button.config(command=lambda: change_node_text())
    update_label_button.place(x=50, y=50)

    cancel_label_button = Button(node_window, text="Cancel")
    cancel_label_button.config(command=lambda: cancel_node_edit())
    cancel_label_button.place(x=50, y=80)



def create_bond_control():
    global bond_label_entry
    bond_window.geometry("200x300")
    bond_window.protocol("WM_DELETE_WINDOW", cancel_bond_edit)
    bond_window.title("Bond Control")

    title_label = Label(bond_window, text="Bond Control Panel")
    title_label.pack()

    bond_label_entry = Entry(bond_window)
    bond_label_entry.pack()

    update_label_button = Button(bond_window, text="Update Label")
    update_label_button.config(command=lambda: change_bond_text())
    update_label_button.place(x=50, y=50)

    cancel_label_button = Button(bond_window, text="Cancel")
    cancel_label_button.config(command=lambda: cancel_bond_edit())
    cancel_label_button.place(x=50, y=80)




def detect_node_selection():
    global node_label_entry
    if screen_ut.pygame_running and (screen_ut.changeable_node is not None):
        if node_window.state() == "withdrawn":
            node_label_entry.delete(0, END)
            node_label_entry.insert(0, screen_ut.node_list[screen_ut.changeable_node].text)
            node_window.deiconify()
    # recheck window after delay
    node_window.after(100, detect_node_selection)


def detect_bond_selection():
    global bond_label_entry
    if screen_ut.pygame_running and (screen_ut.changeable_bond is not None):
        if bond_window.state() == "withdrawn":
            bond_label_entry.delete(0, END)
            bond_label_entry.insert(0, screen_ut.bond_list[screen_ut.changeable_bond].text)
            bond_window.deiconify()
    # recheck window after delay
    bond_window.after(100, detect_bond_selection)




def main():
    global root_window, node_window, bond_window
    print ("Program Running")
    root_window = Tk()
    node_window = Toplevel(root_window)
    bond_window = Toplevel(root_window)

    screen_ut.WIDTH = WIDTH
    screen_ut.HEIGHT = HEIGHT
    start_screen()

    create_root_control()
    create_node_control()
    create_bond_control()

    node_window.withdraw()
    bond_window.withdraw()

    detect_node_selection()
    detect_bond_selection()

    root_window.mainloop()




# Threads
screen_thread = threading.Thread(target=screen_loop)


if __name__ == '__main__':
    main()

