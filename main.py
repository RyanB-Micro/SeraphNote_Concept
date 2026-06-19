import pygame
import os
from tkinter import *
from tkinter import filedialog
import threading
import platform
import screen_utils as screen_ut
import pandas_utils as pandas_ut


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
fact_body_text = None

project_name = "SeraphNote__New_File__.pk1"


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
    global project_name
    new_title = title_label_entry.get().strip()
    if not new_title:
        new_title = "__New_File__"

    project_name = "SeraphNote_" + new_title + ".pk1"
    screen_ut.window_title = project_name


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
    body = str(fact_body_text.get(1.0, END))
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



def delete_node():
    if screen_ut.changeable_node is None:
        return

    deleting_node = screen_ut.node_list[screen_ut.changeable_node]

    screen_ut.delete_item(deleting_node, screen_ut.node_list)
    screen_ut.changeable_node = None

    # Hide window
    node_window.withdraw()


def delete_fact():
    if screen_ut.changeable_fact is None:
        return

    deleting_fact = screen_ut.fact_list[screen_ut.changeable_fact]

    screen_ut.delete_item(deleting_fact, screen_ut.fact_list)
    screen_ut.changeable_fact = None

    # Hide window
    fact_window.withdraw()


def delete_bond():
    if screen_ut.changeable_bond is None:
        return

    deleting_bond = screen_ut.bond_list[screen_ut.changeable_bond]

    screen_ut.delete_bond(deleting_bond)
    screen_ut.changeable_bond = None

    # Hide window
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


# def save_project():
#     change_title_text()
#     # if not project_name:
#     #     project_name = "SeraphNote__New_File__.pk1"
#     save_location = "SeraphNote_Saves/" + project_name
#     pandas_ut.save_project(screen_ut.node_list, screen_ut.fact_list, screen_ut.bond_list, save_location)

def save_project():
    global  project_name
    # get latest project name typed in
    change_title_text()

    # create directory if doest exist
    os.makedirs("SeraphNote_Saves/", exist_ok=True)

    # Ensure a name wass entered
    if len(project_name) < 1:
        project_name = "SeraphNote__New_File__.pk1"

    # Open file location window to save project
    file = filedialog.asksaveasfilename(initialfile=project_name, initialdir="SeraphNote_Saves/", defaultextension=".pk1", filetypes=[("Project File", ".pk1")])
    save_location = file

    # call pickle save function
    pandas_ut.save_project(screen_ut.node_list, screen_ut.fact_list, screen_ut.bond_list, save_location)


def load_project():
    change_title_text()
    file = filedialog.askopenfilename(initialfile=project_name, defaultextension=".pk1", filetypes=[("Project File", ".pk1")])
    save_location = file
    # save_location = "SeraphNote_Saves/" + project_name
    nodes_list_in, facts_list_in, bonds_list_in = pandas_ut.load_project(save_location)
    screen_ut.node_list = nodes_list_in
    screen_ut.fact_list = facts_list_in
    screen_ut.bond_list = bonds_list_in




def create_root_control():
    global title_label_entry
    # bond_num = screen_ut.changeable_node
    root_window.geometry("200x300")
    root_window.protocol("WM_DELETE_WINDOW", quit_all)
    root_window.title("Main Control")

    title_label = Label(root_window, text="Main Control Panel")
    title_label.pack()


    # Project name
    Label(root_window, text="Project Name").pack(anchor="w", pady = (7, 0))
    title_label_entry = Entry(root_window, width=30)
    title_label_entry.pack()

    change_title_button = Button(root_window, text="Update Project Name")
    change_title_button.config(command=lambda: change_title_text())
    change_title_button.place(x=40, y=80)

    # Saving project data
    save_project_button = Button(root_window, text="Save Project -> 💾 ")
    save_project_button.config(command=lambda: save_project())
    save_project_button.place(x=50, y=110)

    # Loading  project data
    load_project_button = Button(root_window, text="💾 -> Load Project")
    load_project_button.config(command=lambda: load_project())
    load_project_button.place(x=50, y=140)

    # Add version labels
    python_version = "Python Ver. " + str(platform.python_version())
    pygame_version = "PyGame Ver. " + str(screen_ut.pygame_version)
    pandas_version = "Pandas Ver. " + str(pandas_ut.pandas_version)
    python_label = Label(root_window, text=python_version)
    python_label.place(x=40, y=200)
    pygame_label = Label(root_window, text=pygame_version)
    pygame_label.place(x=40, y=220)
    pandas_label = Label(root_window, text=pandas_version)
    pandas_label.place(x=40, y=240)



def create_node_control():
    global node_label_entry
    node_window.geometry("200x300")
    node_window.protocol("WM_DELETE_WINDOW", cancel_node_edit)
    node_window.title("Node Control")

    title_label = Label(node_window, text="Node Control Panel")
    title_label.pack()

    Label(node_window, text="Node Name").pack(anchor="w", pady=(7, 0))
    node_label_entry = Entry(node_window, width=30)
    node_label_entry.pack()

    update_label_button = Button(node_window, text="Update Node")
    update_label_button.config(command=lambda: change_node_text())
    update_label_button.place(x=50, y=80)

    cancel_label_button = Button(node_window, text="Cancel")
    cancel_label_button.config(command=lambda: cancel_node_edit())
    cancel_label_button.place(x=60, y=110)


    delete_node_button = Button(node_window, text="Delete Node")
    delete_node_button.config(command=lambda: delete_node())
    delete_node_button.place(x=50, y=250)


def create_fact_control():
    global fact_label_entry, fact_body_text
    fact_window.geometry("200x300")
    fact_window.protocol("WM_DELETE_WINDOW", cancel_fact_edit)
    fact_window.title("Fact Control")

    title_label = Label(fact_window, text="Fact Control Panel")
    title_label.pack()

    Label(fact_window, text="Fact Name").pack(anchor="w", pady=(7, 0))
    fact_label_entry = Entry(fact_window, width=30)
    fact_label_entry.pack()

    Label(fact_window, text="Fact Text").pack(anchor="w", pady=(7, 0))
    fact_body_text = Text(fact_window,height=30, width=30)
    fact_body_text.pack()

    update_label_button = Button(fact_window, text="Update Fact")
    update_label_button.config(command=lambda: change_fact_text())
    update_label_button.place(x=50, y=160)

    cancel_label_button = Button(fact_window, text="Cancel")
    cancel_label_button.config(command=lambda: cancel_fact_edit())
    cancel_label_button.place(x=60, y=190)

    delete_fact_button = Button(fact_window, text="Delete Fact")
    delete_fact_button.config(command=lambda: delete_fact())
    delete_fact_button.place(x=50, y=250)


def create_bond_control():
    global bond_label_entry
    bond_window.geometry("200x300")
    bond_window.protocol("WM_DELETE_WINDOW", cancel_bond_edit)
    bond_window.title("Bond Control")

    title_label = Label(bond_window, text="Bond Control Panel")
    title_label.pack()

    Label(bond_window, text="Bond Name").pack(anchor="w", pady=(7, 0))
    bond_label_entry = Entry(bond_window, width=30)
    bond_label_entry.pack()

    update_label_button = Button(bond_window, text="Update Bond")
    update_label_button.config(command=lambda: change_bond_text())
    update_label_button.place(x=50, y=80)

    cancel_label_button = Button(bond_window, text="Cancel")
    cancel_label_button.config(command=lambda: cancel_bond_edit())
    cancel_label_button.place(x=60, y=110)

    delete_bond_button = Button(bond_window, text="Delete Bond")
    delete_bond_button.config(command=lambda: delete_bond())
    delete_bond_button.place(x=50, y=250)


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

# "For God so loved the world, that he gave his one and only Son, so that whoever believes in him should not perish, but get to live an everlasting life - John 3:16"