import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(stdscr):
    # Clear screen
    stdscr.clear()

    begin_x = 0; begin_y = 0
    height = curses.LINES // 2; width = curses.COLS
    output_window = curses.newwin(height, width, begin_y, begin_x)

    begin_x = 0; begin_y = curses.LINES // 2
    height = curses.LINES // 2; width = curses.COLS
    input_window = curses.newwin(height, width, begin_y, begin_x)

    stdscr.refresh()

    output_window.addstr(0, 0, 'Welcome to my Calc!')
    stdscr.refresh()

    # Input field
    input_window.addstr(0, 0, "Enter math expression:")
    stdscr.refresh()
    box = Textbox(input_window)
    box.edit()
    message = box.gather()

    input_window.addstr(0, 0, message)
    stdscr.refresh()

    var = input('Whatever')
    if var=='q':
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


    stdscr.getkey()


wrapper(main)

