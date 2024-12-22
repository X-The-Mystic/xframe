import sqlite3
import curses
from core import Firewall  # Import the Firewall class

def display_logo(stdscr):
    logo = """                                  
#   # ##### ####  ####  ##### ####  #   #  #### 
#   # #     #   #  #    #     #   #  # #  #     
 #### ####  ####   #### ####  ####    #   #     
    # #     #      #  # #     #      #    #     
    # ##### #     ##### ##### #     #      #### 
    """
    stdscr.addstr(0, 0, logo)

def main_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()
    display_logo(stdscr)
    menu_items = [
        "1: Display Packets",
        "2: Search Packets",
        "3: Settings",
        "4: Help",
        "5: Enable/Disable Firewall",
        "6: View Logs",
        "7: Configure Rules",
        "8: Network Statistics",
        "9: Threat Analysis",
        "10: Exit"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        display_logo(stdscr)
        for idx, item in enumerate(menu_items):
            x = 0
            y = idx + 6
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item)
        stdscr.addstr(len(menu_items) + 8, 0, "Use arrow keys to navigate, Enter to select", curses.color_pair(2))
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == ord('\n'):
            if current_row == len(menu_items) - 1:
                break  # Exit the program
            # Call corresponding functions based on the selected menu item
            handle_menu_selection(current_row)

def handle_menu_selection(selection):
    firewall = Firewall()  # Create an instance of the Firewall class
    if selection == 0:
        firewall.display_packets_loop()  # Call function to display packets
    elif selection == 1:
        search_packets()  # Call function to search packets
    elif selection == 2:
        open_settings()  # Call function for settings
    elif selection == 3:
        display_help()  # Call function to display help
    elif selection == 4:
        firewall.firewall_enabled = not firewall.firewall_enabled
        status = "enabled" if firewall.firewall_enabled else "disabled"
        print(f"Firewall is now {status}.")  # Toggle firewall
    elif selection == 5:
        firewall.view_logs()  # View logs
    elif selection == 6:
        firewall.configure_rules()  # Configure rules
    elif selection == 7:
        firewall.display_statistics()  # Display network statistics
    elif selection == 8:
        firewall.threat_analysis()  # Perform threat analysis

def search_packets():
    print("Searching packets...")  # Implement search packets logic
    # Here you can add logic to search packets in the database

def open_settings():
    print("Opening settings...")  # Implement settings logic
    # Here you can add logic to modify settings

def display_help():
    print("Displaying help...")  # Implement help logic
    # Here you can add logic to display help information

if __name__ == "__main__":
    curses.wrapper(main_menu) 