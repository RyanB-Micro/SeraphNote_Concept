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
fact_window = None
title_label_entry = None
node_label_entry = None
bond_label_entry = None
fact_label_entry = None
fact_body_entry = None

main_title_label = None

slogans = ["Connecting Minds to Thoughts", "For God so loved the world, that he gave his one and only Son, so that whoever believes in him should not perish, but get to live an everlasting life - John 3:16"]


def start_screen():
    global screen_thread
    stop_event.clear()
    screen_thread.start()


def stop_screen():
    global screen_thread
    stop_event.set()
    screen_thread.join(timeout=2)


def quit_all():
    global stop_event
    # Stop pygame parts
    stop_event.set()
    screen_ut.pygame_running = False

    # Stop tk parts
    root_window.quit()
    root_window.destroy()


def screen_loop():
    while not stop_event.is_set():
        if screen_ut.pygame_running == False:
            screen_ut.init_screen(WIDTH, HEIGHT)

        screen_ut.screen_loop()
        # Once screen loop finished -> close thread
        stop_event.set()
        break
        #stop_screen()


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


def change_fact_text():
    if screen_ut.changeable_fact is None:
        return

    label = fact_label_entry.get()
    body = fact_body_entry.get()
    screen_ut.fact_list[screen_ut.changeable_fact].title = label
    screen_ut.fact_list[screen_ut.changeable_fact].text = body
    screen_ut.changeable_fact = None
    fact_window.withdraw()


def change_bond_text():
    if screen_ut.changeable_bond is None:
        return

    text = bond_label_entry.get()
    screen_ut.bond_list[screen_ut.changeable_bond].text = text
    screen_ut.changeable_bond = None
    bond_window.withdraw()


def cancel_node_edit():
    screen_ut.changeable_node = None
    node_window.withdraw()


def cancel_bond_edit():
    screen_ut.changeable_bond = None
    bond_window.withdraw()

def cancel_fact_edit():
    screen_ut.changeable_fact = None
    fact_window.withdraw()


def create_root_control():
    global title_label_entry
    # bond_num = screen_ut.changeable_node
    root_window.geometry("200x300")
    root_window.protocol("WM_DELETE_WINDOW", quit_all)
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


def create_fact_control():
    global fact_label_entry, fact_body_entry
    fact_window.geometry("200x300")
    fact_window.protocol("WM_DELETE_WINDOW", cancel_fact_edit)
    fact_window.title("Node Control")

    title_label = Label(fact_window, text="Fact Control Panel")
    title_label.pack()

    fact_label_entry = Entry(fact_window)
    fact_label_entry.pack()

    fact_body_entry = Entry(fact_window)
    fact_body_entry.pack()

    update_label_button = Button(fact_window, text="Update Fact")
    update_label_button.config(command=lambda: change_fact_text())
    update_label_button.place(x=50, y=100)

    cancel_label_button = Button(fact_window, text="Cancel")
    cancel_label_button.config(command=lambda: cancel_fact_edit())
    cancel_label_button.place(x=50, y=140)



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


def detect_fact_selection():
    global fact_label_entry, fact_body_entry
    if screen_ut.pygame_running and (screen_ut.changeable_fact is not None):
        if fact_window.state() == "withdrawn":
            fact_label_entry.delete(0, END)
            fact_label_entry.insert(0, screen_ut.fact_list[screen_ut.changeable_fact].text)
            fact_window.deiconify()
    # recheck window after delay
    fact_window.after(100, detect_fact_selection)


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
    global root_window, node_window, bond_window, fact_window
    print ("Program Running")
    root_window = Tk()
    node_window = Toplevel(root_window)
    bond_window = Toplevel(root_window)
    fact_window = Toplevel(root_window)

    screen_ut.WIDTH = WIDTH
    screen_ut.HEIGHT = HEIGHT
    start_screen()

    create_root_control()
    create_node_control()
    create_bond_control()
    create_fact_control()

    node_window.withdraw()
    bond_window.withdraw()
    fact_window.withdraw()

    detect_node_selection()
    detect_bond_selection()
    detect_fact_selection()

    root_window.mainloop()

    # Once windows closed -> Make sure thread ends
    if screen_thread.is_alive():
        screen_thread.join()




# Threads
screen_thread = threading.Thread(target=screen_loop)


if __name__ == '__main__':
    main()

