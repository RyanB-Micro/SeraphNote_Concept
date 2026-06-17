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


def main():
    print ("Program Running")
    start_screen()





# Threads
screen_thread = threading.Thread(target=screen_loop)


if __name__ == '__main__':
    main()

