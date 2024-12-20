import sqlite3
import curses
import time

def display_packets(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Connect to the database
    conn = sqlite3.connect("packets.db")
    cursor = conn.cursor()
    
    # Fetch packets
    cursor.execute("SELECT * FROM packets")
    packets = cursor.fetchall()
    
    max_display = 20  # Limit the number of packets displayed
    for i, packet in enumerate(packets[:max_display]):
        try:
            # Display only relevant fields, e.g., src_ip and dst_ip
            display_text = f"Src: {packet[1]}, Dst: {packet[2]}, Proto: {packet[3]}"
            stdscr.addstr(i, 0, display_text[:curses.COLS - 1])  # Truncate to fit the screen
        except curses.error:
            stdscr.addstr(i, 0, "Error displaying packet")
    
    stdscr.refresh()
    
    # Wait for a key press
    stdscr.addstr(len(packets[:max_display]) + 2, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()
    
    # Close the database connection
    conn.close()

def display_menu():
    print("\n--- Firewall Menu ---")
    print("1: Display Packets")
    print("2: Exit")

def main():
    curses.wrapper(display_packets)

if __name__ == "__main__":
    main() 