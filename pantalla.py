import curses

screen = curses.initscr()

curses.curs_set(0)
screen.addstr(20, 30, "Hola Mundo")
screen.addstr(50,30, "Esto es otra cosa")

screen.refresh()
curses.napms(4000)
curses.curs_set(1)
curses.endwin()