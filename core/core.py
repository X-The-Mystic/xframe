import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging (0 = all, 1 = info, 2 = warning, 3 = error)

import threading
import time
from skel.packet_interception import PacketSniffer
from skel.data_preparation import DataPreparation
from skel.neural_network import build_model, train_model, evaluate_model
from skel.feature_extraction import PacketFeatureExtractor
from skel.cli_interface import display_packets, display_menu
from sklearn.preprocessing import StandardScaler
import curses  # Import curses
import sqlite3

class Firewall:
    def __init__(self):
        self.sniffer = PacketSniffer(interface="eth0")  # Change interface as needed
        self.data_preparation = DataPreparation(db_path="packets.db")
        self.feature_extractor = PacketFeatureExtractor()
        self.model = None
        self.scaler = None

    def start_sniffer(self):
        """Start the packet sniffer in a separate thread."""
        sniffer_thread = threading.Thread(target=self.sniffer.start)
        sniffer_thread.start()
        return sniffer_thread

    def train_model(self):
        """Prepare data and train the neural network model."""
        X_train, X_test, y_train, y_test = self.data_preparation.prepare_data()
        self.model = build_model(X_train.shape[1])
        self.model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    def compute_threat_score(self, packet):
        """Compute the threat score for a given packet."""
        features = self.feature_extractor.extract_features(packet)
        features = features.reshape(1, -1)  # Reshape for prediction
        threat_probability = self.model.predict(features)[0][0]
        return threat_probability

    def apply_defense(self, packet):
        """Apply dynamic defense rules based on the computed threat score."""
        score = self.compute_threat_score(packet)
        action = "blocked" if score > 0.5 else "allowed"
        print(f"[{action.upper()}] Packet: {packet}")
        log_packet_decision(packet, score, action)

    def run(self):
        """Run the firewall application."""
        while True:
            display_menu()  # Display the menu
            choice = input("Choose an option (1: Display Packets, 2: Exit): ")
            if choice == '1':
                curses.wrapper(display_packets)  # Wrap display_packets with curses
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.")

def display_packets(stdscr):
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

if __name__ == "__main__":
    firewall = Firewall()
    firewall.run()