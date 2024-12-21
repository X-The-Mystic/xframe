import sqlite3
import curses

def display_packets(stdscr):
    stdscr.clear()
    conn = sqlite3.connect("packets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM packets")
    packets = cursor.fetchall()
    max_display = 20  # Limit the number of packets displayed
    for i, packet in enumerate(packets[:max_display]):
        try:
            display_text = f"Src: {packet[1]}, Dst: {packet[2]}, Proto: {packet[3]}"
            stdscr.addstr(i, 0, display_text[:curses.COLS - 1])
        except curses.error:
            stdscr.addstr(i, 0, "Error displaying packet")
    stdscr.refresh()
    stdscr.addstr(len(packets[:max_display]) + 2, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()
    conn.close()

def display_menu():
    print("\n--- Firewall Menu ---")
    print("1: Display Packets")
    print("2: Exit") 