#!/usr/bin/env python3
"""
Created by: Isaac Hu

Dependencies:
    pyautogui: https://pyautogui.readthedocs.io/
    pynput:    https://pypi.org/project/pynput/
"""
import pyautogui
import time
import threading
import argparse
import textwrap
from pynput import keyboard

"""
Defining global constants and variables here
"""
g_click_change_intv = 0.1   # steps for changing click interval in seconds
g_clicker_enabled = False   # clicker enabled or not
g_hotkey_handler = None     # handler for listening hot keys
g_click_interval = None     # click interval in seconds
g_click_x = None            # x coordinate of clicking position
g_click_y = None            # y coordinate of clicking position
g_quit_thread = False       # flag to notify quiting clicking thread


def enable_clicker():
    """
    Function to response to the hot key for enabling clicker thread
    :return:
    """
    global g_clicker_enabled

    g_clicker_enabled = True    # clicker enabled
    print('Enabling the clicker...')


def disable_clicker():
    """
    Function to response to the hot key for disabling clicker thread
    :return:
    """
    global g_clicker_enabled

    g_clicker_enabled = False   # clicker disabled
    print('Disabling the clicker...')


def click_mouse_left():
    """
    Thread function to emulate mouse left clicking
    :return:
    """
    global g_clicker_enabled
    global g_click_interval
    global g_click_x
    global g_click_y
    global g_quit_thread

    # thread running in loops until the flag changes to quit
    while not g_quit_thread:
        # start emulating mouse clicking if variable is set to enable clicking
        if g_clicker_enabled:
            pyautogui.moveTo(g_click_x, g_click_y)
            pyautogui.click()
            print('Move mouse to {}, {}'.format(g_click_x, g_click_y))
            pyautogui.mouseDown()
            print('mouseDown')
            time.sleep(0.1)
            pyautogui.mouseUp()
            print("mouseUp")

        time.sleep(g_click_interval)
        print('Wait for {} secs for another click...'.format(g_click_interval))

    print('Quiting mouse click thread...')


def increase_click_intv():
    """
    Function to response hot key for reducing click interval
    :return:
    """
    global g_click_interval
    global g_click_change_intv

    g_click_interval += g_click_change_intv
    # set maximum clicking interval to 5 secs
    if g_click_interval > 5:
        g_click_interval = 5
    print('Increasing the clicking speed to {}...'.format(g_click_interval))


def decrease_click_intv():
    """
    Function to response hot key for increasing click interval
    :return:
    """
    global g_click_interval
    global g_click_change_intv

    g_click_interval -= g_click_change_intv
    # set minimum interval to 0.1 secs
    if g_click_interval < 0.1:
        g_click_interval = 0.1
    print('Decreasing the clicking speed to {}...'.format(g_click_interval))


def quit_clicker():
    """
    Function to response hot key for quiting the program
    :return:
    """
    global g_hotkey_handler

    print('Exiting the clicker...')
    g_hotkey_handler.stop()


if __name__ == "__main__":
    """
    Main entrance/thread of the script
    """
    #
    # Initialising clicker parameters
    #
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent("""
    Hot keys to control the programs:
        <cmd>+<shift>+s: Enable clicker
        <cmd>+<shift>+p: Disable clicker
        <cmd>+<shift>+]: Increase speed
        <cmd>+<shift>+[: Decrease speed
        <cmd>+<shift>+;: Quit clicker
    """))
    parser.add_argument('-s', '--speed', type=float, default=0.1, dest="click_interval",
                        help='Clicking interval in seconds')
    parser.add_argument('-x', '--xpos', type=int, default=None, dest="click_x_pos",
                        help='X position on the screen where the clicker clicks. If no input, the program clicks at the horizontal centre of the screen.')
    parser.add_argument('-y', '--ypos', type=int, default=None, dest="click_y_pos",
                        help='Y position on the screen where the clicker clicks. If no input, the program clicks at the vertical centre of the screen.')
    args = parser.parse_args()
    g_click_interval = args.click_interval
    screen_size = pyautogui.size()

    if args.click_x_pos is None:
        # set the default clicking position to the horizontal centre of the screen
        g_click_x = screen_size.width / 2
    else:
        g_click_x = args.click_x_pos

    if args.click_y_pos is None:
        # set the default clicking position to the vertical centre of the screen
        g_click_y = screen_size.height / 2
    else:
        g_click_y = args.click_y_pos

    print('Clicking interval: {}'.format(g_click_interval))
    print('Clicking x coordinate: {}'.format(g_click_x))
    print('Clicking y coordinate: {}'.format(g_click_y))

    #
    # Starting the mouse clicking thread
    #
    click_thread = threading.Thread(target=click_mouse_left)
    click_thread.start()

    #
    # Initialising hot keys of the clicker
    #
    with keyboard.GlobalHotKeys({
        '<cmd>+<shift>+s': enable_clicker,
        '<cmd>+<shift>+p': disable_clicker,
        '<cmd>+<shift>+]': increase_click_intv,
        '<cmd>+<shift>+[': decrease_click_intv,
        '<cmd>+<shift>+;': quit_clicker}) as g_hotkey_handler:
        g_hotkey_handler.join()

    #
    # Quiting program
    #
    g_quit_thread = True
    click_thread.join()
    print('Program completed.')